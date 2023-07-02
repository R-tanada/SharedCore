#ifndef USBDEVICEIMPL_H
#define USBDEVICEIMPL_H

#include <libusb.h>

#include "USBDeviceDescription.h"

#include <functional>
#include <unordered_map>
#include <atomic>
#include <thread>
#include <mutex>

namespace avatarflow {
namespace media {

/** DeviceConnectedCallback
 * @brief Connected callback datatype
 */
using DeviceConnectedCallback = std::function<void(const avatarflow::media::USBDeviceDescription &desc)>;

/** DeviceDisconnectedCallback
 * @brief Disconnected callback datatype
 */
using DeviceDisconnectedCallback = std::function<void(const avatarflow::media::USBDeviceDescription &desc)>;

class USBDeviceImpl {
public:
    USBDeviceImpl();
    USBDeviceImpl(DeviceConnectedCallback connectedCallback, DeviceDisconnectedCallback disconnectedCallback);
    ~USBDeviceImpl();

    /** setConnectedCallback
     * @brief Setter function for connected callback
     * @param @ref DeviceConnectedCallback callback object
     */
    void setConnectedCallback(DeviceConnectedCallback callback);

    /** setDisconnectedCallback
     * @brief Setter function for disconnected callback
     * @param @ref DeviceDisconnectedCallback callback object
     */
    void setDisconnectedCallback(DeviceDisconnectedCallback callback);

private:
    /** init
     * @brief initializing function for libusb library
     */
    void init();

    /** usbConnected
     * @brief Connected callback function libusb event
     * @param libusb_context Context that event occured
     * @param libusb_device Connected device
     * @param libusb_hotplug_event Connected event
     * @param user_data Data that stored on callback registery
     */
    static int usbConnected(struct libusb_context *ctx, struct libusb_device *dev,
                            libusb_hotplug_event event, void *user_data);
    
    /** usbDisconnected
     * @brief Disconnected callback function libusb event
     * @param libusb_context Context that event occured
     * @param libusb_device Disconnected device
     * @param libusb_hotplug_event Disconnected event
     * @param user_data Data that stored on callback registery
     */
    static int usbDisconnected(struct libusb_context *ctx, struct libusb_device *dev,
                               libusb_hotplug_event event, void *user_data);
    
    /** deviceID
     * @brief Device id generator function for connected devices
     * @param libusb_device Connected device
     * @return Generated device id
     */
    static std::uint16_t deviceID(struct libusb_device *device);

    /** getDeviceDescription
     * @brief Device info of the event
     * @param libusb_device Connected device
     * @return @ref USBDeviceDescription object
     */
    static USBDeviceDescription getDeviceDescription(struct libusb_device *device);

private:
    DeviceConnectedCallback mConnectedCallback;
    DeviceDisconnectedCallback mDisconnectedCallback;

    libusb_hotplug_callback_handle mConnectedCallbackHandle;
    libusb_hotplug_callback_handle mDisconnectedCallbackHandle;

    std::atomic<bool> mStopThread;
    std::thread mThread;
    std::mutex mMutex;
    std::unordered_map<std::uint16_t, avatarflow::media::USBDeviceDescription> mAttachedDevices;
};

}
}

#endif // USBDEVICEIMPL_H
