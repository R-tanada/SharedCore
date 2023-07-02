
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

#ifndef AUTHENTICATIONMANAGER_H
#define AUTHENTICATIONMANAGER_H

#include "flow/avatarflow_config.h"
#include "utils/ISingleton.h"
#include "utils/ListenerContainer.h"

#include <functional>

namespace utils {
class IRequest;
}

namespace avatarflow {
namespace engine {

/**
 * @brief The Token class Data class for Authentication Token
 */
class AvaFlow_API Token {
public:
  Token();
  Token(const std::string &accessToken, const std::string &tokenType,
        std::uint32_t expiresIn, const std::string &scope);

  /**
   * @brief GetAccessToken Returns the access token
   * @return String value of the access token
   */
  const std::string &GetAccessToken() const noexcept;

  /**
   * @brief GetTokenType Returns the token type
   * @return String value of the token type
   */
  const std::string &GetTokenType() const noexcept;

  /**
   * @brief GetExpiresIn Returns the expiresIn value for the token
   * @return Uint32 value for the expiresIn
   */
  std::uint32_t GetExpiresIn() const noexcept;

  /**
   * @brief GetScope Returns the scope of the token
   * @return String value of the scope
   */
  const std::string GetScope() const noexcept;

  /**
   * @brief SetAccessToken Sets the access token value
   * @param accessToken String value of the access token
   */
  void SetAccessToken(const std::string &accessToken) noexcept;

  /**
   * @brief SetTokenType Sets the token type
   * @param tokenType String value of the token type
   */
  void SetTokenType(const std::string &tokenType) noexcept;

  /**
   * @brief SetExpiresIn Sets the exipresIn value
   * @param expiresIn UInt32 value of the expiresIn
   */
  void SetExpiresIn(std::uint32_t expiresIn) noexcept;

  /**
   * @brief SetScope Sets the scope of the token
   * @param scope String value of the scope
   */
  void SetScope(const std::string &scope) noexcept;

  /**
   * @brief toString Returns the token object in JSON string
   * @return String value of the token
   */
  const std::string toString() const noexcept;

private:
  std::string mAccessToken;
  std::string mTokenType;
  std::uint32_t mExpiresIn;
  std::string mScope;
};

/**
 * @brief The AuthenticationManagerListener class Listener Interface Class for
 * the Authentication events
 */
class AuthenticationManagerListener {
public:
  /**
   * @brief onAuthenticated Callback on successfull authentication
   * @param token Token object for received access tokem
   */
  virtual void onAuthenticated(const Token &token) = 0;

  /**
   * @brief onError Callback for errors
   * @param message String value of the error message
   */
  virtual void onError(const std::string &message) = 0;
};

/**
 * @brief The AuthenticationManager class Authentication Manager for requesting
 * Authentication token and dispatching to the listeners
 */
class AvaFlow_API AuthenticationManager
    : public utils::ISingleton<AuthenticationManager>,
      public utils::ListenerContainer<AuthenticationManagerListener *> {
public:
  using AuthenticationCallback = std::function<void(const Token &token)>;
  using ErrorCallback = std::function<void(const std::string &message)>;

public:
  AuthenticationManager(const std::string &username,
                        const std::string &password);
  ~AuthenticationManager() noexcept;

  /**
   * @brief SetAuthenticationCallback Sets the callback for successful
   * authentication
   * @param callback Callback object
   */
  void SetAuthenticationCallback(const AuthenticationCallback &callback);

  /**
   * @brief SetErrorCallback Sets the callback for errors on authentication
   * process
   * @param callback Callback object
   */
  void SetErrorCallback(const ErrorCallback &callback);

  /**
   * @brief Authenticate Makes request for authentication
   */
  void Authenticate() const noexcept;

  /**
   * @brief GetToken Returns access token object
   * @return Returns the access token, if it is not authanticated access token
   * will be empty
   */
  const Token &GetToken() const noexcept;

private:
  DECLARE_FIRE_METHOD(onAuthenticated, (const Token &token), (token));
  DECLARE_FIRE_METHOD(onError, (const std::string &message), (message));

private:
  static const std::string tag;
  const std::string mUsername;
  const std::string mPassword;
  Token mToken;
  AuthenticationCallback mAuthCallback;
  ErrorCallback mErrorCallback;
  utils::IRequest *mRequest;
};
} // namespace engine
} // namespace avatarflow

#endif // AUTHENTICATIONMANAGER_H
