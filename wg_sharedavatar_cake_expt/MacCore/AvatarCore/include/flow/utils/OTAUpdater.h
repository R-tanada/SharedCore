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

#ifndef __OTAUPDATER__
#define __OTAUPDATER__

#include "flow/avatarflow_config.h"
#include <string>
#include <utils/GUID.h>
#include <utils/JSONUtils.h>


namespace utils {

class OTAUpdaterImpl;

class AvaFlow_API OTAUpdater {
private:
  OTAUpdaterImpl *_impl;

public:
  static const utils::GUID PATH_DownloadStatus;
  static const utils::GUID PATH_FetchedVersion;

public:
  OTAUpdater(/* args */);
  ~OTAUpdater();

  bool LoadConfig(const std::string &config);
  bool LoadConfigJSON(JSONObject config);
  void SetUpdateChannel(const std::string &channel, const std::string &branch);

  void Start();
  void Stop();
  bool IsRunning();

  const std::string &GetLatestVersion();
  const std::string &GetUpdateURL();

  bool IsDownloadAvailable();
  void StartManualDownload();
};
} // namespace utils

#endif //__OTAUPDATER__