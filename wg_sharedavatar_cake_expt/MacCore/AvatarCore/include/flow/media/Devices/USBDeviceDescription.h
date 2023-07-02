#ifndef USBDEVICEDESCRIPTION_H
#define USBDEVICEDESCRIPTION_H

#include <cinttypes>
#include <string>

namespace avatarflow {
namespace media {

/** USB Device Descriptor
 * @brief
 */
struct USBDeviceDescription {
    /** Device Pointer
     * @brief pointer that is return by libusb, cast to libusb_device * to use with libusb
     */
    void *dev;

    /** USB Descriptor Type
     * @brief data holder for @ref libusb_descriptor_type
     */
    std::uint8_t descriptorType;

    /** USB Specification Release Number
     * @brief Binary coded decimal value for release number.
     * 0x0110 for USB 1.1, 0x0200 for USB 2.0
     */
    std::uint16_t releaseNumber;

    /** Device Class
     * @brief USB-IF class code for the device @ref libusb_class_code
     */
    std::uint8_t deviceClass;

    /** Device Subclass
     * @brief USB-IF subclass code for the device
     */
    std::uint8_t deviceSubClass;

    /** Device Protocol
     * @brief USB-IF protocol for the device
     */
    std::uint8_t protocol;

    /** Max Packet Size
     * @brief Max packet size for endpoint 0
     */
    std::uint8_t maxPacketSize0;

    /** Vendor ID
     * @brief USB-IF device vendor id
     */
    std::uint16_t vendorID;

    /** Product ID
     * @brief USB-IF product id
     */
    std::uint16_t productID;

    /** Device Release Number
     * @brief Binary coded decimal for device release number
     */
    std::uint16_t deviceReleaseNumber;

    /** Manufacturer
     * @brief Manufacturer string descriptor
     */
    std::string manufacturer;

    /** Product
     * @brief Product string descriptor
     */
    std::string product;

    /** Serial Number
     * @brief Device serial number string descriptor
     */
    std::string serialNumber;

    /** Configurations
     * @brief Number of possible configurations
     */
    std::uint8_t configurations;
};

}
}

#endif // USBDEVICEDESCRIPTION_H
