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

#ifndef __CONTINUOUSADAPTIVEVIDEOSTREAMER__
#define __CONTINUOUSADAPTIVEVIDEOSTREAMER__

#include "IAdaptiveVideoStreamer.h"
#include <utils/Tween.h>

namespace avatarflow {
namespace media {
class ContinuousAdaptiveVideoStreamer : public IAdaptiveVideoStreamer {
private:
  /* data */
  std::string _name;

  utils::DTween _qualTween;
  float _currQual;
  float _initialQual;

  float _sizeScaler;

  float _minScaler;
  int _scalerStep;
  float _interpolator;
  float _qosMinThreshold;
  float _qosMaxThreshold;

  int _MinBitrate;
  int _MaxBitrate;

  int _bitrate;

public:
  ContinuousAdaptiveVideoStreamer(const std::string &name);
  virtual ~ContinuousAdaptiveVideoStreamer();

  virtual bool OnQoS(const QOSFeedback &qos);
  virtual void Reset();
  virtual void Update(float dt);

  virtual float GetCurrQuality();
  virtual int GetBitrate();
  virtual int GetWidth(int currWidth);
  virtual int GetHeight(int currHeight);

  virtual bool Parse(const JSONObject &stream);
};

} // namespace media
} // namespace avatarflow

#endif //__CONTINUOUSADAPTIVEVIDEOSTREAMER__