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

#ifndef __OTAUpdateService__
#define __OTAUpdateService__

#include "IService.h"
#include "utils/IDelegate.h"

namespace avatarflow {
namespace services {

class OTAUpdateServiceImpl;
class AvaFlow_API OTAUpdateService : public IService {
public:
  DECLARE_RTTI

protected:
  OTAUpdateServiceImpl *_impl;

  static const utils::GUID PATH_RequestUpdate;

public:
  OTAUpdateService(/* args */);
  virtual ~OTAUpdateService();

  virtual bool Init(ServiceContext *context);
  virtual bool StartService();
  virtual bool StopService();
  virtual bool IsRunning();

  virtual void LoadSettings(const JSONObject &settings);
  virtual void Subscriber_OnMessage(const utils::GUID &serviceName,
                                    const utils::GUID &path,
                                    const std::string &data,
                                    utils::uint address, bool forwarded);
};
MAKE_SERVICE_FACTORY(OTAUpdateService, "OTAUpdate")

} // namespace services
} // namespace avatarflow

#endif //__OTAUpdateService__