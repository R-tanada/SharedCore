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

#ifndef BLACKBOARDSHAREDMEMORY_H
#define BLACKBOARDSHAREDMEMORY_H

#include "IBlackboard.h"
#include "ListenerContainer.h"
#include "OSType.h"
#include "avatarutils_config.h"

namespace utils {

#ifdef __MOBILE__
class MobileBlackboardSharedMemoryImpl;
typedef MobileBlackboardSharedMemoryImpl BlackboardType;
#else
class BlackboardSharedMemoryImpl;
typedef BlackboardSharedMemoryImpl BlackboardType;

#endif
class BlackboardSharedMemoryListener {

public:
  /**
   * @brief The State enum holds the current state of the Blackbox Shared Memory
   */
  enum class State {
    initialized,
    destroyed,
    set,
    value_removed,
    category_removed,
    category_cleared,
    blackboard_cleared
  };

  /**
   * @brief onStateChaged Callback for state changed notification
   * @param state Value of the current state
   */
  virtual void onStateChanged(const State state) = 0;
};

/**
 * @brief The BlackboardSharedMemory class Shared Memory implementation for
 * Blackboard
 */
class AvaUtils_API BlackboardSharedMemory
    : public IBlackboard,
      public ListenerContainer<BlackboardSharedMemoryListener *> {

public:
  BlackboardSharedMemory();
  /**
   * @brief BlackboardSharedMemory Creates a memory file with given name.
   * If a file is already exists with given name it removes then creates a new
   * file.
   * @param memoryName Name of the memory file
   */
  BlackboardSharedMemory(const std::string &memoryName);
  ~BlackboardSharedMemory() noexcept;

  BlackboardSharedMemory(const BlackboardSharedMemory &) = delete;
  BlackboardSharedMemory &operator=(const BlackboardSharedMemory &) = delete;
  BlackboardSharedMemory(BlackboardSharedMemory &&) = delete;
  BlackboardSharedMemory &operator=(BlackboardSharedMemory &&) = delete;

  /**
   * @brief Initialize Initialize Initializes the shared memory. It is used for
   * late initialization If given name exists it returns false. It will fire
   * initialization event on successful creation.
   * @param memoryName Name of the memory file
   * @return Returns true if the operation successful, false otherwise
   */
  bool Initialize(const std::string &memoryName);

  DECLARE_FIRE_METHOD(onStateChanged,
                      (const BlackboardSharedMemoryListener::State state),
                      (state));

  // IBlackboard interface
public:
  virtual bool SetValue(const std::string &category, const std::string &key,
                        const std::string &value) final override;
  virtual std::string GetValue(const std::string &category,
                               const std::string &key,
                               const std::string &defaultValue) final override;
  virtual bool IsValueExist(const std::string &category,
                            const std::string &key) final override;
  virtual std::unordered_map<std::string, std::string>
  GetValues(const std::string &category) final override;
  virtual std::vector<std::string> GetCategories() final override;
  virtual std::unordered_map<std::string,
                             std::unordered_map<std::string, std::string>>
  GetData() final override;
  virtual void Clear() final override;
  virtual void Clear(const std::string &category) final override;
  virtual void Remove(const std::string &category) final override;
  virtual void Remove(const std::string &category,
                      const std::string &key) final override;

private:
  BlackboardType *mImpl;
};
} // namespace utils

#endif // BLACKBOARDSHAREDMEMORY_H
