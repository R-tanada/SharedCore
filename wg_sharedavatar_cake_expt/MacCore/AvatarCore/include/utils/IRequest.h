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

#ifndef IREQUEST_H
#define IREQUEST_H

#include "ListenerContainer.h"

#include <functional>
#include <mutex>
#include <thread>
#include <unordered_map>

namespace Poco {
class Exception;
namespace Net {
class HTTPRequest;
}
} // namespace Poco

namespace utils {

class HTTPRequestBuilder;

class HTTPRequestListener {
public:
  /**
   * @brief onResponse function for HTTP Response
   * @param status Status code for HTTP Response
   * @param response body of the HTTP Response in string format
   */
  virtual void onResponse(int status, const std::string &response) const = 0;

  /**
   * @brief onError Callback function for any error occurs during sending a
   * request
   * @param exception Poco exception pointer
   */
  virtual void onError(const Poco::Exception &exception) const = 0;
};

/**
 * @brief The HTTPRequest class for handling HTTP Requests
 */
class IRequest : public ListenerContainer<HTTPRequestListener *> {
private:
  friend class HTTPRequestBuilder;

public:
  using HTTPHeaders = std::unordered_map<std::string, std::string>;
  using OnResponse =
      std::function<void(int status, const std::string &response)>;
  using OnError = std::function<void(const Poco::Exception &exception)>;

public:
  virtual ~IRequest() noexcept;

protected:
  IRequest();
  IRequest(const std::string &uri, std::uint16_t timeout = 60,
           bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           std::uint16_t timeout = 60, bool keepAlive = false,
           HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           const std::string &method, std::uint16_t timeout = 60,
           bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           const std::string &method, const std::string &version,
           std::uint16_t timeout = 60, bool keepAlive = false,
           HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           const std::string &method, const std::string &version,
           const HTTPHeaders &headers, std::uint16_t timeout = 60,
           bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           const std::string &method, const std::string &version,
           const HTTPHeaders &headers, const OnResponse &onResponse,
           std::uint16_t timeout = 60, bool keepAlive = false,
           HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           const std::string &method, const std::string &version,
           const HTTPHeaders &headers, const OnResponse &onResponse,
           const OnError &onError, std::uint16_t timeout = 60,
           bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  IRequest(const std::string &uri, const std::string &contentType,
           const std::string &method, const std::string &version,
           const HTTPHeaders &headers, const OnResponse &onResponse,
           const OnError &onError, const std::string &body,
           std::uint16_t timeout = 60, bool keepAlive = false,
           HTTPRequestListener *listener = nullptr);

protected:
  IRequest(const IRequest &other);
  // IRequest operator = (const IRequest &other);
  IRequest(IRequest &&other) noexcept;
  // IRequest operator = (IRequest &&other) noexcept;

  /**
   * @brief SetURI Sets the URI of the request
   * @param uri string value of the URI
   */
  void SetURI(const std::string &uri) const noexcept;

  /**
   * @brief AddHeader Adds request headers
   * @param name Name of the HTTP Header
   * @param value Value of the header
   */
  void AddHeader(const std::string &name,
                 const std::string &value) const noexcept;

  /**
   * @brief SetContentType Sets the content type of the HTTP Request
   * @param type Content Type value
   */
  void SetContentType(const std::string &contentType) const noexcept;

  /**
   * @brief SetHTTPMethod Sets the HtTP method
   * @param method Method enum
   */
  void SetHTTPMethod(const std::string &method) const noexcept;

  /**
   * @brief SetHTTPVersion Sets the HTTP version
   * @param version Poco version string
   */
  void SetHTTPVersion(const std::string &version) const noexcept;

  /**
   * @brief SetTimeout Sets the timeout value of the request
   * @param timeout Timeout value in seconds
   */
  void SetTimeout(std::uint16_t timeout) noexcept;

  /**
   * @brief SetKeepAlive Sets the keepAlive state of the request
   * @param keepAlive Boolean value of the keepAlive dafult is false
   */
  void SetKeepAlive(bool keepAlive = false) const noexcept;

  /**
   * @brief SetRequestBody Sets the body of the request
   * @param body String value of the body
   */
  void SetRequestBody(const std::string &body) noexcept;

  DECLARE_FIRE_METHOD(onResponse, (int status, const std::string &response),
                      (status, response));
  DECLARE_FIRE_METHOD(onError, (const Poco::Exception &exception), (exception));

public:
  /**
   * @brief SetOnResponseCallback Sets the callback for OnResponse
   * @param callback OnResponse callback object
   */
  void SetOnResponseCallback(const OnResponse &callback) noexcept;

  /**
   * @brief SetOnErrorCallback Sets the callback for OnError event
   * @param callback OnError callback object
   */
  void SetOnErrorCallback(const OnError &callback) noexcept;

  /**
   * @brief URI Gets the URI of the request
   * @return String value of the URI
   */
  const std::string &URI() const noexcept;

  /**
   * @brief send Executes blocking HTTP Request. If and error occurs during
   * sending a request or receiving a response throws a Poco::Exception
   * @return Returns the response body as a string
   */
  virtual const std::string send() const = 0;

  /**
   * @brief sendAsync Executes non-blocking HTTP Request. On receiving a
   * response it will fire OnResponse event in as a callback or/and function in
   * HTTPRequestListener. On an error during send or receive it will fire
   * OnError
   */
  virtual void sendAsync() = 0;

private:
  std::string mURI;
  std::string mContentType;
  std::string mMethod;
  std::string mVersion;
  HTTPHeaders mHTTPHeaders;
  HTTPRequestListener *mListener;
  static const std::string tag;

protected:
  std::uint16_t mTimeout;
  bool mKeepAlive;
  OnResponse mOnResponseCallback;
  OnError mOnErrorCallback;
  std::string mBody;
  std::mutex mMutex;
  std::thread mThread;
  Poco::Net::HTTPRequest *mRequest;
};
} // namespace utils

#endif // IREQUEST_H
