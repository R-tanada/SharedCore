/************************************************************************
 *                                                                      *
 * Copyright 2022 AvatarIn Inc. Tokyo, Japan. All Rights Reserved       *
 *                                                                      *
 *       _____               __               .___                      *
 *      /  _  \___  ______ _/  |______ _______|   | ____                *
 *     /  /_\  \  \/ |__  \\   __\__  \\_  __ \   |/    \               *
 *    /    |    \   / / __ \|  |  / __ \|  | \/   |   |  \              *
 *    \____|__  /\_/ (____  /__| (____  /__|  |___|___|  /              *
 *            \/          \/          \/               \/               *
 *                                                                      *
 * Developed by: Eren Dogus Ates                                        *
 ************************************************************************/

#ifndef BLACKBOARDSHAREDMEMORYIMPL_H
#define BLACKBOARDSHAREDMEMORYIMPL_H

#define BOOST_UNORDERED_USE_ALLOCATOR_TRAITS 1
#define BOOST_UNORDERED_CXX11_CONSTRUCTION 1

#include <boost/container/scoped_allocator.hpp>
#include <boost/functional/hash/extensions.hpp>
#include <boost/interprocess/allocators/allocator.hpp>
#include <boost/interprocess/containers/string.hpp>
#include <boost/interprocess/managed_shared_memory.hpp>
#include <boost/unordered_map.hpp>
#include <unordered_map>

#include <string>

namespace utils {

/**
 * @brief The BlackboardSharedMemoryImpl class Blackboard Shared Memory
 * implementation details
 */
class BlackboardSharedMemoryImpl {
public:
  BlackboardSharedMemoryImpl();
  /**
   * @brief BlackboardSharedMemoryImpl Creates a shared memory file with given
   * name. It will try to open the file if exists or I will create a new file
   * If it is not able to open the file or create a new one it will throw
   * an exception.
   * @param memoryName Name of the shared memory file.
   */
  BlackboardSharedMemoryImpl(const std::string &memoryName);
  ~BlackboardSharedMemoryImpl() noexcept;

  BlackboardSharedMemoryImpl(const BlackboardSharedMemoryImpl &) = delete;
  BlackboardSharedMemoryImpl &
  operator=(const BlackboardSharedMemoryImpl &) = delete;
  BlackboardSharedMemoryImpl(BlackboardSharedMemoryImpl &&) = delete;
  BlackboardSharedMemoryImpl &operator=(BlackboardSharedMemoryImpl &&) = delete;

  /**
   * @brief Initialize Initializes the shared memory. It is used for late
   * initialization, It will try to open the file if exists or I will create a
   * new file If it is not able to open the file or create a new one it will
   * return false.
   * @param memoryName Name of the shared memory file.
   * @return Returns true if operation is succesful, false otherwise
   */
  bool Initialize(const std::string &memoryName);

  bool SetValue(const std::string &category, const std::string &key,
                const std::string &value);
  std::string GetValue(const std::string &category, const std::string &key,
                       const std::string &defaultValue = "");
  bool IsValueExist(const std::string &category, const std::string &key);
  std::unordered_map<std::string, std::string>
  GetValues(const std::string &category);
  std::vector<std::string> GetCategories();
  std::unordered_map<std::string, std::unordered_map<std::string, std::string>>
  GetData();
  void Clear();
  void Clear(const std::string &category);
  void Remove(const std::string &category);
  void Remove(const std::string &category, const std::string &key);

private:
  using Segment = boost::interprocess::managed_shared_memory;
  using Manager = Segment::segment_manager;

  template <typename T>
  using Alloc = boost::interprocess::allocator<T, Manager>;
  template <typename T>
  using ScopedAlloc = boost::container::scoped_allocator_adaptor<Alloc<T>>;

  template <typename K, typename V, typename KH = boost::hash<K>,
            typename KEq = std::equal_to<K>>
  using SharedMap =
      boost::unordered_map<K, V, KH, KEq, ScopedAlloc<std::pair<const K, V>>>;

  using String = boost::interprocess::basic_string<char, std::char_traits<char>,
                                                   ScopedAlloc<char>>;

  using Category = SharedMap<String, String>;
  using Blackboard = SharedMap<String, Category>;

  static const std::string tag;
  static const std::string mObjectName;
  static const std::uint32_t mMemorySize;
  static const std::string mFileRefCounter;
  static const std::string mMutexTag;
  std::string mMemoryName;
  std::string mMutexName;

  Segment mManagedMemoryManager;
};
} // namespace utils

#endif // BLACKBOARDSHAREDMEMORYIMPL_H
