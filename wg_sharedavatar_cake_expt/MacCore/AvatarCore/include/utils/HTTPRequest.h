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

#ifndef HTTPREQUEST_H
#define HTTPREQUEST_H

#include "IRequest.h"

namespace utils {

class HTTPRequest : public IRequest {
private:
  friend class HTTPRequestBuilder;

protected:
  HTTPRequest();
  HTTPRequest(const std::string &uri, std::uint16_t timeout = 60,
              bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              std::uint16_t timeout = 60, bool keepAlive = false,
              HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              const std::string &method, std::uint16_t timeout = 60,
              bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              const std::string &method, const std::string &version,
              std::uint16_t timeout = 60, bool keepAlive = false,
              HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              const std::string &method, const std::string &version,
              const HTTPHeaders &headers, std::uint16_t timeout = 60,
              bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              const std::string &method, const std::string &version,
              const HTTPHeaders &headers, const OnResponse &onResponse,
              std::uint16_t timeout = 60, bool keepAlive = false,
              HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              const std::string &method, const std::string &version,
              const HTTPHeaders &headers, const OnResponse &onResponse,
              const OnError &onError, std::uint16_t timeout = 60,
              bool keepAlive = false, HTTPRequestListener *listener = nullptr);
  HTTPRequest(const std::string &uri, const std::string &contentType,
              const std::string &method, const std::string &version,
              const HTTPHeaders &headers, const OnResponse &onResponse,
              const OnError &onError, const std::string &body,
              std::uint16_t timeout = 60, bool keepAlive = false,
              HTTPRequestListener *listener = nullptr);

  virtual ~HTTPRequest();

  // IRequest interface
public:
  virtual const std::string send() const override;
  virtual void sendAsync() override;

private:
  static const std::string tag;
};
} // namespace utils

#endif // HTTPREQUEST_H
