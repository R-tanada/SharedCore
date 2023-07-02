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

#ifndef __AUDIOFORMAT__
#define __AUDIOFORMAT__

#include "flow/avatarflow_config.h"
#include "utils/atypes.h"

namespace avatarflow {
namespace media {

enum AudioFormat {
  AF_Unkown,
  AF_U8,
  AF_S8,
  AF_U16,
  AF_S16,
  AF_U24,
  AF_S24,
  AF_U32,
  AF_S32,
  AF_F32,
  AF_F64,
};
enum AudioFormatFlags {
  EAudioFlags_Signed = BIT(0),
  EAudioFlags_FloatingPoint = BIT(1)
};

struct AudioFormatDescriptor {
public:
  std::string name;
  AudioFormat type;

  utils::uchar size; // element Size in bytes
  utils::uint flags; // see AudioFormatFlags
};

class AvaFlow_API AudioUtils {
public:
  static const AudioFormatDescriptor &GetFormatDescriptor(AudioFormat f);

  static std::string GetGstFormat(AudioFormat fmt, bool bigEndian);
};

} // namespace media
} // namespace avatarflow

#endif //__AUDIOFORMAT__