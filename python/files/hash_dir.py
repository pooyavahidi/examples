import os
import hashlib
import time


class HashDir:
    def __init__(self, dir_path):
        self.files = []
        self.hash_alg = "md5"
        self.dir_path = dir_path

    def __get_hasher(self):
        # Todo: implement the multi hash algorithm
        # return hashlib.sha256()
        return hashlib.md5()

    def __load_files(self, path):
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                self.files.append(os.path.join(r, file))

    def __hash_file(self, filepath, chunk_size=2**20):
        hasher = self.__get_hasher()
        with open(filepath, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                hasher.update(data)
            hash_val = hasher.digest()
        return hash_val

    def hash_dir(self):
        hashes = []
        self.__load_files(self.dir_path)
        for f in self.files:
            hash_val = self.__hash_file(f)
            hashes.append(f.replace(self.dir_path, "") + hash_val.hex())

        # sort and combine the hash values to create the final hash
        hashes.sort(key=str.lower)
        hashes_combined = bytes("".join(hashes), "utf-8")
        print(f"Calculated hash for {len(hashes)} files")
        dir_hash_val = hashlib.sha256(hashes_combined)

        return dir_hash_val

    def hash_dir_multiprocess(self, dir_path, number_of_processes=4):
        # to be implemented later using subprocesses or multiprocessing
        pass


if __name__ == "__main__":
    path = os.getcwd()
    start = time.time()
    hash_dir = HashDir(path)
    hash_val = hash_dir.hash_dir()
    print(f"{hash_val.hexdigest()}  {path}")
    duration = time.time() - start
    print(f"processing time: {duration} secs")
