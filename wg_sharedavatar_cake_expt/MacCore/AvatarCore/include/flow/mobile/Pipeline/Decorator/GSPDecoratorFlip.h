#ifndef GSPIPELINE_DECORATOR_FLIP_HPP
#define GSPIPELINE_DECORATOR_FLIP_HPP

#include <iostream>

#include "../Builder/GSPDecoratorBuilder.h"
#include "GSPipelineDecorator.h"

namespace avatarflow {
namespace media {

class GSPDecoratorFlip : public GSPipelineDecorator {
    friend class GSPDecoratorBuilder;

   public:
    virtual ~GSPDecoratorFlip();

    GstElement* decorate();

   protected:
    GSPDecoratorFlip(IGSPipeline* inner, const gchar *eleName, int flipMethod);

    const gchar *mElementName;
    const int mFlipMethod;
};
}  // namespace media
}  // namespace avatarflow
#endif
