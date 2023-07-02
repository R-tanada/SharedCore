#ifndef AVATAR_MESSAGE_HELPER_H
#define AVATAR_MESSAGE_HELPER_H

#include <mobile/DataWrap.h>

namespace avatarmobile
{
    class AvatarMessageHelperImpl;

    class AvatarMessageHelper
    {
    private:
        AvatarMessageHelperImpl* _impl;
    public:
        
        // To avoid repeated if else
        float  forwardMove;
        float  strideMove;
        float  neckMove;
        
        int  batteryLevel;
        bool isCharging;
        int  remainingTime;
    public:
        AvatarMessageHelper(DataWrap*d);
        ~AvatarMessageHelper();


        void sendAvatarIn();
        void sendReservation(const std::string& resId);
        void updateMove();
        void updateNeck();
        std::string parseJson (const std::string& json);
        
    };

} // namespace avatarmobile

#endif
