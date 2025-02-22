#include <mayaUsd/utils/loadRules.h>

#include <gtest/gtest.h>

PXR_NAMESPACE_USING_DIRECTIVE

TEST(ConvertLoadRules, convertEmptyLoadRules)
{
    UsdStageLoadRules originalLoadRules;

    const MString text = MayaUsd::convertLoadRulesToText(originalLoadRules);

    UsdStageLoadRules convertedLoadRules = MayaUsd::createLoadRulesFromText(text);

    EXPECT_EQ(originalLoadRules, convertedLoadRules);
}

TEST(ConvertLoadRules, convertSimpleLoadRules)
{
    UsdStageLoadRules originalLoadRules;
    originalLoadRules.AddRule(SdfPath("/a/b/c"), UsdStageLoadRules::AllRule);
    originalLoadRules.AddRule(SdfPath("/a/b"), UsdStageLoadRules::NoneRule);
    originalLoadRules.AddRule(SdfPath("/d"), UsdStageLoadRules::OnlyRule);

    const MString text = MayaUsd::convertLoadRulesToText(originalLoadRules);

    UsdStageLoadRules convertedLoadRules = MayaUsd::createLoadRulesFromText(text);

    EXPECT_EQ(originalLoadRules, convertedLoadRules);
}

TEST(ConvertLoadRules, convertEmptyStageLoadRules)
{
    auto originalStage = UsdStage::CreateInMemory();

    const MString text = MayaUsd::convertLoadRulesToText(*originalStage);

    auto convertedStage = UsdStage::CreateInMemory();
    MayaUsd::setLoadRulesFromText(*convertedStage, text);

    EXPECT_EQ(originalStage->GetLoadRules(), convertedStage->GetLoadRules());
}

TEST(ConvertLoadRules, convertSimpleStageLoadRules)
{
    UsdStageLoadRules originalLoadRules;
    originalLoadRules.AddRule(SdfPath("/a/b/c"), UsdStageLoadRules::AllRule);
    originalLoadRules.AddRule(SdfPath("/a/b"), UsdStageLoadRules::NoneRule);
    originalLoadRules.AddRule(SdfPath("/d"), UsdStageLoadRules::OnlyRule);
    originalLoadRules.AddRule(SdfPath("/d/e"), UsdStageLoadRules::AllRule);
    auto originalStage = UsdStage::CreateInMemory();
    originalStage->SetLoadRules(originalLoadRules);

    const MString text = MayaUsd::convertLoadRulesToText(*originalStage);

    auto convertedStage = UsdStage::CreateInMemory();
    MayaUsd::setLoadRulesFromText(*convertedStage, text);

    EXPECT_EQ(originalStage->GetLoadRules(), convertedStage->GetLoadRules());
}
