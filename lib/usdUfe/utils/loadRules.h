//
// Copyright 2022 Autodesk
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
#ifndef USDUFE_LOADRULES_H
#define USDUFE_LOADRULES_H

#include <usdUfe/base/api.h>

#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/stage.h>

namespace USDUFE_NS_DEF {

/*! \brief modify the stage load rules so that the rules governing fromPath are replicated for
 * destPath.
 */
USDUFE_PUBLIC
void duplicateLoadRules(
    PXR_NS::UsdStage&      stage,
    const PXR_NS::SdfPath& fromPath,
    const PXR_NS::SdfPath& destPath);

/*! \brief modify the stage load rules so that all rules governing the path are removed.
 */
USDUFE_PUBLIC
void removeRulesForPath(PXR_NS::UsdStage& stage, const PXR_NS::SdfPath& path);

} // namespace USDUFE_NS_DEF

#endif
