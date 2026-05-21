import { Hero } from "../components/Hero";
import { FeatureSkillDemo } from "../components/FeatureSkillDemo";
import { FeatureTodoGuardrail } from "../components/FeatureTodoGuardrail";
import { FeatureStressTest } from "../components/FeatureStressTest";
import { FeatureMultiAgent } from "../components/FeatureMultiAgent";
import { FeatureEnhanceMe } from "../components/FeatureEnhanceMe";
import { FeatureDeepSleep } from "../components/FeatureDeepSleep";
import { ROISection } from "../components/ROISection";
import { BottomCTA } from "../components/BottomCTA";

export function Home() {
  return (
    <>
      <Hero />
      <div id="features">
        <FeatureSkillDemo />
        <FeatureTodoGuardrail />
        <FeatureEnhanceMe />
        <FeatureStressTest />
        <FeatureDeepSleep />
        <FeatureMultiAgent />
      </div>
      <ROISection />
      <BottomCTA />
    </>
  );
}
