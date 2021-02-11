from abc import ABC, abstractmethod
import numpy as np
import sys

class RageHash(ABC):
    NAME_MAX = 64 # maximum length including terminating character

    @staticmethod
    def _name_next(n, len):
        for i in range(len):
            if n[i] >= ord('z'):
                #overflow
                n[i] = ord('_')
                continue
            elif n[i] == ord('_'):
                # skip '`'
                n[i] = ord('a')
            else:
                n[i] = n[i] + 1
            return True
        return False

    @abstractmethod
    def _gpu_init(self):
        pass

    @abstractmethod
    def _gpu_brute9(self, base_name, skip, hash):
        pass

    def main(self):
        print("Thanks to xSonoro & XeClutch for their work.")
        print("")

        if len(sys.argv) != 4:
            print("Invalid argument count.")
            return

        hash = int(sys.argv[1], 16)
        len_min = int(sys.argv[2])
        len_max = min(self.NAME_MAX - 1, max(len_min, int(sys.argv[3])))

        if len_min < 9:
            print("Minimum length needs to be at least 9")
            return

        self._gpu_init()

        base_name = np.empty(self.NAME_MAX, dtype=np.uint8)
        base_name.fill(ord('_'))

        print("Solving hash: 0x{:02x}".format(hash))

        for len_full in range(len_min, len_max + 1):
            print("  Length: {: <2}".format(len_full))
            len_pref = len_full - 9
            while True:
                sys.stdout.flush()
                self._gpu_brute9(base_name, len_pref, hash)
                if not self._name_next(base_name, len_pref):
                    break

        print("Done.")
