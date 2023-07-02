/************************************************************************
 *                                                                      *
 * Copyright 2020 AvatarIn Inc. Tokyo, Japan. All Rights Reserved       *
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

#ifndef __AVATARINHTTPREQUESTBUILDER__
#define __AVATARINHTTPREQUESTBUILDER__

#include "HTTPRequestBuilder.h"

namespace utils {

/**
 * @brief Derived from HTTPRequestBuilder, providing the required headers to
 * invoke a request to avatarin backend
 *
 */
class AvaUtils_API avatarinHTTPRequestBuilder : public HTTPRequestBuilder {
private:
  std::string _environment;
  std::string _serverURL;

  static const std::string sAuthorization;
  static const std::string sUserAgent;

public:
  avatarinHTTPRequestBuilder(const std::string &env = "");
  virtual ~avatarinHTTPRequestBuilder() noexcept;

  // remove non-required operators
  avatarinHTTPRequestBuilder(const avatarinHTTPRequestBuilder &) = delete;
  avatarinHTTPRequestBuilder
  operator=(const avatarinHTTPRequestBuilder &) = delete;
  avatarinHTTPRequestBuilder(const avatarinHTTPRequestBuilder &&) = delete;
  avatarinHTTPRequestBuilder operator=(avatarinHTTPRequestBuilder &&) = delete;

  /**
   * @brief Set the Backend Environment to be used
   *
   * @param env: dev/uat/prod
   * @return utils::avatarinHTTPRequestBuilder&
   */
  utils::avatarinHTTPRequestBuilder &SetEnvironment(const std::string &env);

  const std::string &envGetEnvironment() const { return _environment; }

  /**
   * @brief Specify the API request needed without specifying the server.
   *
   *
   * @param api requested API path, e.g. to request login API\: /login
   */
  utils::avatarinHTTPRequestBuilder &SetRequestAPI(const std::string &api);

  /**
   * @brief Get the URL of the server selected
   *
   * @return const std::string&
   */
  const std::string &GetServerURL() const { return _serverURL; }
};

} // namespace utils

#endif //__AVATARINHTTPREQUESTBUILDER__