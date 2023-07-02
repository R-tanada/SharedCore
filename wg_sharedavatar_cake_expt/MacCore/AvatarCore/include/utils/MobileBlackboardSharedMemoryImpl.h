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
 * Developed by: Yamen Saraiji                                          *
 ************************************************************************/

#ifndef MOBILEBLACKBOARDSHAREDMEMORYIMPL_H
#define MOBILEBLACKBOARDSHAREDMEMORYIMPL_H

#include <string>
#include <unordered_map>
#include <vector>

namespace utils {

/**
 * @brief The MobileBlackboardSharedMemoryImpl class Blackboard Shared Memory
 * implementation details
 */
class MobileBlackboardImplMeta;
class MobileBlackboardSharedMemoryImpl {
public:
  MobileBlackboardSharedMemoryImpl();
  MobileBlackboardSharedMemoryImpl(const std::string &memoryName);
  ~MobileBlackboardSharedMemoryImpl() noexcept;

  MobileBlackboardSharedMemoryImpl(const MobileBlackboardSharedMemoryImpl &) =
      delete;
  MobileBlackboardSharedMemoryImpl &
  operator=(const MobileBlackboardSharedMemoryImpl &) = delete;
  MobileBlackboardSharedMemoryImpl(MobileBlackboardSharedMemoryImpl &&) =
      delete;
  MobileBlackboardSharedMemoryImpl &
  operator=(MobileBlackboardSharedMemoryImpl &&) = delete;

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
  MobileBlackboardImplMeta *_memory;
};
} // namespace utils

#endif // MOBILEBLACKBOARDSHAREDMEMORYIMPL_H
