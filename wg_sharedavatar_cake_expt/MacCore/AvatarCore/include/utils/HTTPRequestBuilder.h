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

#ifndef HTTPREQUESTBUILDER_H
#define HTTPREQUESTBUILDER_H

#include "IRequest.h"
#include "avatarutils_config.h"

namespace utils {

enum class HTTPMethod {
  HTTP_GET,
  HTTP_HEAD,
  HTTP_PUT,
  HTTP_POST,
  HTTP_OPTIONS,
  HTTP_DELETE,
  HTTP_TRACE,
  HTTP_CONNECT,
  HTTP_PATCH
};

enum class HTTPVersion { HTTP_1_0, HTTP_1_1 };

/**
 * @brief The HTTPRequestBuilder class Builder class for HTTPRequests
 */
class AvaUtils_API HTTPRequestBuilder {
public:
  HTTPRequestBuilder();
  virtual ~HTTPRequestBuilder() noexcept;
  HTTPRequestBuilder(const HTTPRequestBuilder &) = delete;
  HTTPRequestBuilder operator=(const HTTPRequestBuilder &) = delete;
  HTTPRequestBuilder(const HTTPRequestBuilder &&) = delete;
  HTTPRequestBuilder operator=(HTTPRequestBuilder &&) = delete;

  /**
   * @brief SetURI Sets the URI for the request
   * @param uri String value of the URI
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetURI(const std::string &uri) noexcept;

  /**
   * @brief SetOnResponseCallback Sets the OnResponse callback for non-blocking
   * request
   * @param callback IRequest::OnResponse callback object
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &
  SetOnResponseCallback(const IRequest::OnResponse &callback) noexcept;

  /**
   * @brief SetOnErrorCallback Sets the OnError callback for non-blocking
   * request
   * @param callback IRequest::OnError callback object
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &
  SetOnErrorCallback(const IRequest::OnError &callback) noexcept;

  /**
   * @brief SetListener Sets the HTTPRequestListener for non-blocking request
   * @param listener Pointer of the HTTPRequestListener object
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetListener(HTTPRequestListener *listener) noexcept;

  /**
   * @brief SetHTTPMethod Sets the HTTP method for the request
   * @param method HTTPMethod enum
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetHTTPMethod(const HTTPMethod method) noexcept;

  /**
   * @brief SetHTTPVersion Sets the HTTP version of the request
   * @param version HTTPVersion enum
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetHTTPVersion(const HTTPVersion version) noexcept;

  /**
   * @brief AddHeader Adds the name value pair into request header
   * @param name String value of the header name
   * @param value String value of the header value
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &AddHeader(const std::string &name,
                                const std::string &value) noexcept;

  /**
   * @brief SetContentType Sets the content type of the request
   * @param contentType String value of the content type
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetContentType(const std::string &contentType) noexcept;

  /**
   * @brief SetRequestBody Sets the body of the request
   * @param body String value of the body
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetRequestBody(const std::string &body) noexcept;

  /**
   * @brief SetTimeout Sets the timeout value of the request
   * @param timeout Timeout in seconds
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetTimeout(std::uint16_t timeout) noexcept;

  /**
   * @brief SetKeepAlive Sets the keepAlive value of the request
   * @param keepAlive boolean value of the keepAlive
   * @return Returns the rvalue of the HTTPRequestBuilder object
   */
  HTTPRequestBuilder &SetKeepAlive(bool keepAlive) noexcept;

  /**
   * @brief build Constructs the HTTPRequest object
   * @return Pointer of the constructed object in IRequest type;
   * user is responsible to destroy the pointer
   */
  IRequest *build() noexcept;

private:
  std::string mURI;
  IRequest::OnResponse mOnResponse;
  IRequest::OnError mOnError;
  HTTPRequestListener *mListener;
  HTTPMethod mMethod;
  HTTPVersion mVersion;
  std::string mPocoMethod;
  std::string mPocoVersion;
  IRequest::HTTPHeaders mHeaders;
  std::string mContentType;
  std::string mBody;
  std::uint16_t mTimeout;
  bool mKeepAlive;
};
} // namespace utils

#endif // HTTPREQUESTBUILDER_H
