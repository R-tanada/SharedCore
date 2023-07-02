#ifndef USBDEVICE_H
#define USBDEVICE_H

#include <utils/ListenerContainer.h>

#include "USBDeviceDescription.h"

namespace avatarflow {
namespace media {

/** USBDeviceImpl
 * @brief Forward declaration of USBDevice implementation detatils.
 */
class USBDeviceImpl;

/** USBDeviceListener
 * @brief Event listener interface class for USB Notifications
 */
class USBDeviceListener { //Interface class for USB hotplug events
public:
    virtual ~USBDeviceListener() {}
    
    /** onDeviceInserted
     * @brief Callback event on USB Device inserted notification
     * @param @ref avatarflow::media::USBDeviceDescription inserted device information
     */
    virtual void onDeviceInserted(const avatarflow::media::USBDeviceDescription &deviceDesc) = 0;
    
    /** onDeviceRemoved
     * @brief Callback event on USB Device removed notification
     * @param @ref avatarflow::media::USBDeviceDescription removed device information
     */
    virtual void onDeviceRemoved(const avatarflow::media::USBDeviceDescription &deviceDesc) = 0;
    
};

/** USBDevice
 * @brief Class for handling USB notifications and device interractions
 */
class USBDevice : public utils::ListenerContainer<USBDeviceListener *> {
public:
    USBDevice();
    ~USBDevice();

    DECLARE_FIRE_METHOD(onDeviceInserted, (const avatarflow::media::USBDeviceDescription &deviceDesc), (deviceDesc));
    DECLARE_FIRE_METHOD(onDeviceRemoved, (const avatarflow::media::USBDeviceDescription &deviceDesc), (deviceDesc));

private:
    void usbConnected(const avatarflow::media::USBDeviceDescription &desc);
    void usbDisconnected(const avatarflow::media::USBDeviceDescription &desc);
private:
    USBDeviceImpl *mUSBDeviceImpl;
};

}
}
#endif // USBDEVICE_H
