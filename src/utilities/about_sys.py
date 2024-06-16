import sys
import os
import time
import psutil
import unittest


class SystemConfig:
    @staticmethod
    def get_current_timestamp():
        current_time = time.time()
        readable_time = time.ctime(current_time)
        return current_time, readable_time

    @staticmethod
    def get_python_info():
        return sys.version, sys.platform, sys.prefix

    @staticmethod
    def get_cpu_count():
        return os.cpu_count()

    @staticmethod
    def get_current_directory():
        return os.getcwd()

    @staticmethod
    def list_directory():
        return os.listdir()

    @staticmethod
    def get_memory_info():
        memory = psutil.virtual_memory()
        return memory.total, memory.available, memory.used, memory.percent

    @staticmethod
    def get_disk_info():
        partitions = psutil.disk_partitions()
        disk_info = {}
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    'total': partition_usage.total,
                    'used': partition_usage.used,
                    'free': partition_usage.free,
                    'percent': partition_usage.percent
                }
            except PermissionError:
                continue
        return disk_info

    @staticmethod
    def print_config():
        # Print current timestamp
        current_time, readable_time = SystemConfig.get_current_timestamp()
        print("Current timestamp:", current_time)
        print("Readable time:", readable_time)

        # Print Python version and platform information
        python_version, platform, prefix = SystemConfig.get_python_info()
        print("Python version:", python_version)
        print("Platform:", platform)
        print("Prefix:", prefix)

        # Print CPU count
        cpu_count = SystemConfig.get_cpu_count()
        print("CPU Count:", cpu_count)

        # Print current working directory
        current_directory = SystemConfig.get_current_directory()
        print("Current Working Directory:", current_directory)

        # Print memory usage details
        total_mem, avail_mem, used_mem, mem_percent = SystemConfig.get_memory_info()
        print(f"Total Memory: {total_mem} bytes")
        print(f"Available Memory: {avail_mem} bytes")
        print(f"Used Memory: {used_mem} bytes")
        print(f"Memory Usage: {mem_percent}%")

        # Print disk information
        disk_info = SystemConfig.get_disk_info()
        for device, info in disk_info.items():
            print(f"Disk {device}:")
            print(f"  Total: {info['total']} bytes")
            print(f"  Used: {info['used']} bytes")
            print(f"  Free: {info['free']} bytes")
            print(f"  Usage: {info['percent']}%")

        # Understand Directory
        files = SystemConfig.list_directory()
        for file in files:
            print(file)


class TestSystemConfig(unittest.TestCase):
    def test_get_current_timestamp(self):
        current_time, readable_time = SystemConfig.get_current_timestamp()
        self.assertIsInstance(current_time, float)
        self.assertIsInstance(readable_time, str)

    def test_get_python_info(self):
        version, platform, prefix = SystemConfig.get_python_info()
        self.assertIsInstance(version, str)
        self.assertIsInstance(platform, str)
        self.assertIsInstance(prefix, str)

    def test_get_cpu_count(self):
        cpu_count = SystemConfig.get_cpu_count()
        self.assertIsInstance(cpu_count, int)
        self.assertGreater(cpu_count, 0)

    def test_get_current_directory(self):
        current_directory = SystemConfig.get_current_directory()
        self.assertIsInstance(current_directory, str)
        self.assertTrue(os.path.isdir(current_directory))

    def test_list_directory(self):
        files = SystemConfig.list_directory()
        self.assertIsInstance(files, list)
        for file in files:
            self.assertIsInstance(file, str)

    def test_get_memory_info(self):
        total_mem, avail_mem, used_mem, mem_percent = SystemConfig.get_memory_info()
        self.assertIsInstance(total_mem, int)
        self.assertIsInstance(avail_mem, int)
        self.assertIsInstance(used_mem, int)
        self.assertIsInstance(mem_percent, float)
        self.assertGreater(total_mem, 0)
        self.assertGreater(avail_mem, 0)
        self.assertGreater(used_mem, 0)
        self.assertGreaterEqual(mem_percent, 0)
        self.assertLessEqual(mem_percent, 100)

    def test_get_disk_info(self):
        disk_info = SystemConfig.get_disk_info()
        for device, info in disk_info.items():
            self.assertIsInstance(device, str)
            self.assertIsInstance(info['total'], int)
            self.assertIsInstance(info['used'], int)
            self.assertIsInstance(info['free'], int)
            self.assertIsInstance(info['percent'], float)
            self.assertGreater(info['total'], 0)
            self.assertGreater(info['used'], 0)
            self.assertGreater(info['free'], 0)
            self.assertGreaterEqual(info['percent'], 0)
            self.assertLessEqual(info['percent'], 100)


if __name__ == "__main__":
    # Print the system configuration
    SystemConfig.print_config()

    # Run unit tests
    unittest.main(argv=[''], exit=False)
