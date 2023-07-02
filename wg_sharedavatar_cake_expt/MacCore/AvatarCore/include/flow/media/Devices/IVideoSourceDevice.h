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

#ifndef __IVIDEOSOURCEDEVICE__
#define __IVIDEOSOURCEDEVICE__

#include <utils/ListenerContainer.h>
#include <utils/PropertySet.h>
#include <utils/StringUtil.h>

#include <string>

#include "../GStreamer/GstPipeline.h"
#include "flow/media/helpers/PixelFormat.h"

namespace avatarflow {
namespace media {

class IVideoSourceDevice;
class IVideoSourceDeviceListener {
public:
  virtual void OnVideoDeviceOpen(IVideoSourceDevice *device) {}
  virtual void OnVideoDeviceClose(IVideoSourceDevice *device) {}
  virtual void OnVideoDeviceEOS(IVideoSourceDevice *device) {}
  virtual void OnVideoDeviceFrameCaptured(IVideoSourceDevice *device, int w,
                                          int h, PixelFormat format) {}
};

class IVideoSourceDevice
    : public utils::ListenerContainer<IVideoSourceDeviceListener *>,
      public utils::PropertySet {
  DECLARE_RTTI
protected:
  std::string _srcName;
  void *_appsrc;
  GstPipeline *_pipeline;

  DECLARE_FIRE_METHOD(OnVideoDeviceOpen, (IVideoSourceDevice * device),
                      (device))
  DECLARE_FIRE_METHOD(OnVideoDeviceClose, (IVideoSourceDevice * device),
                      (device))
  DECLARE_FIRE_METHOD(OnVideoDeviceEOS, (IVideoSourceDevice * device), (device))
  DECLARE_FIRE_METHOD(OnVideoDeviceFrameCaptured,
                      (IVideoSourceDevice * device, int w, int h,
                       PixelFormat format),
                      (device, w, h, format))

  void _OnFrameCaptured(int w, int h, PixelFormat format) {
    FIRE_LISTENR_METHOD(OnVideoDeviceFrameCaptured, (this, w, h, format));
  }

public:
  IVideoSourceDevice() {
    _appsrc = 0;
    _pipeline = 0;
  }
  virtual ~IVideoSourceDevice() {}

  virtual bool Open() {
    FIRE_LISTENR_METHOD(OnVideoDeviceOpen, (this));
    return true;
  }
  virtual void Close() { FIRE_LISTENR_METHOD(OnVideoDeviceClose, (this)); }

  /**
   * @brief Indicates if this device is ready for use (can output images yet or
   * not). Some devices may requires some time to start ouputing samples.
   * Override to report that
   *
   * @return true
   * @return false
   */
  virtual bool IsReady() { return true; }

  /**
   * @brief returns the gstreamer pipeline string to build this element
   *
   * @param name: name used to construct the capture element (should be unique
   * in the pipeline)
   * @return std::string
   */
  virtual std::string BuildPipeline(const std::string &name) {
    _srcName = name;
    return "";
  }
  /**
   * @brief Populate the needed elements from gstreamer pipeline
   *
   * @param pipeline
   */
  virtual void LinkWithPipeline(GstPipeline *pipeline) {
    _appsrc = pipeline->GetElementByName(_srcName);
    _pipeline = pipeline;
  }

  /**
   * @brief Updates the internal capture settings (after LoadSettings for
   * example)
   *
   * @return true: Success
   * @return false: Failure
   */
  virtual bool UpdateSettings() { return true; }
  /**
   * @brief Does this device requires the service to stop on EOS
   *
   * @return true
   * @return false
   */
  virtual bool StopOnEOS() { return false; }
};

class IVideoSourceDeviceFactory {
public:
  virtual ~IVideoSourceDeviceFactory() {}
  virtual std::string GetType() = 0;
  virtual IVideoSourceDevice *Create() = 0;
};

#define MAKE_VIDEOSOURCEDEVICE_FACTORY(type, name)                             \
  class type##Factory : public IVideoSourceDeviceFactory {                     \
  public:                                                                      \
    virtual std::string GetType() { return name; }                             \
    virtual IVideoSourceDevice *Create() { return new type(); }                \
  };
} // namespace media
} // namespace avatarflow

#endif //__IVIDEOSOURCEDEVICE__