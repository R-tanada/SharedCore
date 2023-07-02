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

#ifndef __LOOKUPADAPTIVEVIDEOSTREAMER__
#define __LOOKUPADAPTIVEVIDEOSTREAMER__

#include "IAdaptiveVideoStreamer.h"
#include <utils/Tween.h>
#include <vector>

namespace avatarflow {
namespace media {

class LookupAdaptiveVideoStreamer : public IAdaptiveVideoStreamer {
private:
  class AdaptiveLevel {
  public:
    AdaptiveLevel() {}
    bool operator<(const AdaptiveLevel &o) const { return qual < o.qual; }
    bool operator==(const AdaptiveLevel &o) const { return qual == o.qual; }

    float qual;
    int width;
    int height;
    int bitrate;
  };

  std::vector<AdaptiveLevel> _levels;

  /* data */
  std::string _name;

  utils::DTween _qualTween;
  float _currQual;
  float _initialQual;
  float _interpolator;
  float _qosMinThreshold;
  float _qosMaxThreshold;

  int _currLevel;

  int GetClosestLevel(float qual);

public:
  LookupAdaptiveVideoStreamer(const std::string &name);
  virtual ~LookupAdaptiveVideoStreamer();

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

#endif //__LOOKUPADAPTIVEVIDEOSTREAMER__