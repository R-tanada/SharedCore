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

#ifndef IBLACKBOARD_H
#define IBLACKBOARD_H

#include <string>
#include <unordered_map>
#include <vector>

namespace utils {

/**
 * @brief IBlackboard Interface class for Blackboard Class
 */
class IBlackboard {
public:
  /**
   * @brief SetValue set the value for given key in a given category
   * @param category category name for the key-value pair
   * @param key key name
   * @param value
   * @return returns true if the operation is succesful, false otherwise
   */
  virtual bool SetValue(const std::string &category, const std::string &key,
                        const std::string &value) = 0;

  /**
   * @brief GetValue get the value for given category and key
   * @param category category name
   * @param key key name
   * @param defaultValue return value if the given category-key pair does not
   * exists
   * @return returns the value for the given category-key pair, othrewise
   * returns the defaultValue
   */
  virtual std::string GetValue(const std::string &category,
                               const std::string &key,
                               const std::string &defaultValue = "") = 0;

  /**
   * @brief GetValues Gets the all values for given category
   * @param category Name of the category
   * @return Returns the map of keys and values, if category does not exist it
   * will return empty map
   */
  virtual std::unordered_map<std::string, std::string>
  GetValues(const std::string &category) = 0;

  /**
   * @brief IsValueExist checks the given category-key pair exists or not
   * @param category category name
   * @param key key name
   * @return returns true if the category-key pair exists, false otherwise
   */
  virtual bool IsValueExist(const std::string &category,
                            const std::string &key) = 0;

  /**
   * @brief GetCategories returns the vector of categories that is in the
   * blackboard
   * @return Returns vector of strings
   */
  virtual std::vector<std::string> GetCategories() = 0;

  /**
   * @brief GetData returns the whole blackboard data
   * @return Returns nested std::unoredred_map
   */
  virtual std::unordered_map<std::string,
                             std::unordered_map<std::string, std::string>>
  GetData() = 0;
  /**
   * @brief Clear Removes the all data from blackboard
   */
  virtual void Clear() = 0;

  /**
   * @brief Clear Clears all data from given category, but keeps the categary
   * intact
   * @param category Name of the category
   */
  virtual void Clear(const std::string &category) = 0;

  /**
   * @brief Remove Removes all data from given category
   * @param category Name of the category
   */
  virtual void Remove(const std::string &category) = 0;

  /**
   * @brief Remove Removes the data with given category and key pair
   * @param category Name of the category
   * @param key Name of the key
   */
  virtual void Remove(const std::string &category, const std::string &key) = 0;
};

} // namespace utils

#endif // IBLACKBOARD_H
