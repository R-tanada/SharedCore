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

#ifndef __RESOURCERECORDER__
#define __RESOURCERECORDER__

#include "flow/avatarflow_config.h"
#include <string>
#include <utils/JSONUtils.h>

namespace avatarflow {
namespace media {

class ResourceRecorderImpl;
class VideoFrame;
class AudioFrame;
class DataFrame;

class AvaFlow_API ResourceRecorder {
private:
  ResourceRecorderImpl *_impl;

public:
  ResourceRecorder(/* args */);
  ~ResourceRecorder();

  void Start();
  void Stop();

  bool AddVideoFrame(const media::VideoFrame *frame, const std::string &shmem);
  bool AddAudioFrame(const media::AudioFrame *frame, const std::string &shmem);
  bool AddDataFrame(const media::DataFrame *frame, const std::string &shmem,
                    const std::string &channelName);

  bool ParseJsonFile(const std::string &filename);
  bool ParseJSON(JSONObject json);
};

} // namespace media
} // namespace avatarflow

#endif //__RESOURCERECORDER__