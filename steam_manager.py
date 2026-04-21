import os
import sys
import ctypes

class SteamManager:
    def __init__(self):
        self.initialized = False
        self._dll = None
        self._stats = None

    @property
    def is_ready(self):
        """Helper property to check if steam is usable"""
        return self.initialized and self._stats is not None

    def init(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            dll_path = os.path.join(base_path, "steam_api64.dll")
            
            if not os.path.exists(dll_path):
                print(f"[Steam] DLL not found at: {dll_path}")
                return

            self._dll = ctypes.CDLL(dll_path)

            self._dll.SteamAPI_Init.restype = ctypes.c_bool
            self._dll.SteamAPI_RunCallbacks.restype = None
            self._dll.SteamAPI_Shutdown.restype = None

            if not self._dll.SteamAPI_Init():
                print("[Steam] SteamAPI_Init failed. Is Steam running?")
                return

            self._dll.SteamAPI_SteamUserStats_v012.restype = ctypes.c_void_p
            self._stats = self._dll.SteamAPI_SteamUserStats_v012()
            
            if not self._stats:
                print("[Steam] Failed to get UserStats interface")
                return

            self._dll.SteamAPI_ISteamUserStats_RequestCurrentStats.restype = ctypes.c_bool
            self._dll.SteamAPI_ISteamUserStats_RequestCurrentStats.argtypes = [ctypes.c_void_p]
            
            self._dll.SteamAPI_ISteamUserStats_SetAchievement.restype = ctypes.c_bool
            self._dll.SteamAPI_ISteamUserStats_SetAchievement.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            
            self._dll.SteamAPI_ISteamUserStats_StoreStats.restype = ctypes.c_bool
            self._dll.SteamAPI_ISteamUserStats_StoreStats.argtypes = [ctypes.c_void_p]
            
            self._dll.SteamAPI_ISteamUserStats_GetAchievement.restype = ctypes.c_bool
            self._dll.SteamAPI_ISteamUserStats_GetAchievement.argtypes = [
                ctypes.c_void_p, 
                ctypes.c_char_p, 
                ctypes.POINTER(ctypes.c_bool)
            ]

            self._dll.SteamAPI_ISteamUserStats_RequestCurrentStats(self._stats)
            self.initialized = True
            print("[Steam] Initialized successfully")
            
        except Exception as e:
            print(f"[Steam] Failed to initialize: {e}")
            self.initialized = False

    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        if not self.is_ready:
            return False
            
        try:
            achieved = ctypes.c_bool(False)
            success = self._dll.SteamAPI_ISteamUserStats_GetAchievement(
                self._stats, 
                achievement_id.encode('utf-8'), 
                ctypes.byref(achieved)
            )
            return success and achieved.value
        except Exception as e:
            print(f"[Steam] Error checking achievement: {e}")
            return False

    def run_callbacks(self):
        if not self.initialized:
            return
        try:
            self._dll.SteamAPI_RunCallbacks()
        except Exception as e:
            print(f"[Steam] Callback error: {e}")

    def unlock_achievement(self, achievement_id: str):
        if not self.initialized:
            return
        try:
            result = self._dll.SteamAPI_ISteamUserStats_SetAchievement(
                self._stats,
                achievement_id.encode('utf-8')
            )
            self._dll.SteamAPI_ISteamUserStats_StoreStats(self._stats)
            print(f"[Steam] Achievement unlocked: {achievement_id} (result={result})")
        except Exception as e:
            print(f"[Steam] Achievement error: {e}")

    def write_cloud_file(self, filename: str, data: bytes):
        if not self.initialized:
            return False
        try:
            self._dll.SteamAPI_SteamRemoteStorage_v014.restype = ctypes.c_void_p
            storage = self._dll.SteamAPI_SteamRemoteStorage_v014()

            self._dll.SteamAPI_ISteamRemoteStorage_FileWrite.restype = ctypes.c_bool
            self._dll.SteamAPI_ISteamRemoteStorage_FileWrite.argtypes = [
                ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int32
            ]
            result = self._dll.SteamAPI_ISteamRemoteStorage_FileWrite(
                storage,
                filename.encode('utf-8'),
                data,
                len(data)
            )
            print(f"[Steam] Cloud write '{filename}': {result}")
            return result
        except Exception as e:
            print(f"[Steam] Cloud write error: {e}")
            return False

    def read_cloud_file(self, filename: str) -> bytes | None:
        if not self.initialized:
            return None
        try:
            self._dll.SteamAPI_SteamRemoteStorage_v014.restype = ctypes.c_void_p
            storage = self._dll.SteamAPI_SteamRemoteStorage_v014()

            self._dll.SteamAPI_ISteamRemoteStorage_GetFileSize.restype = ctypes.c_int32
            self._dll.SteamAPI_ISteamRemoteStorage_GetFileSize.argtypes = [
                ctypes.c_void_p, ctypes.c_char_p
            ]
            size = self._dll.SteamAPI_ISteamRemoteStorage_GetFileSize(
                storage, filename.encode('utf-8')
            )
            if size == 0:
                return None

            self._dll.SteamAPI_ISteamRemoteStorage_FileRead.restype = ctypes.c_int32
            self._dll.SteamAPI_ISteamRemoteStorage_FileRead.argtypes = [
                ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int32
            ]
            buf = ctypes.create_string_buffer(size)
            self._dll.SteamAPI_ISteamRemoteStorage_FileRead(
                storage, filename.encode('utf-8'), buf, size
            )
            print(f"[Steam] Cloud read '{filename}': {size} bytes")
            return buf.raw
        except Exception as e:
            print(f"[Steam] Cloud read error: {e}")
            return None

steam = SteamManager()