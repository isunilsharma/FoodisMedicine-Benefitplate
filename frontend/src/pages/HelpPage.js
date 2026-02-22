import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';

const HelpPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Help & FAQ</h1>
          <p className="text-gray-600">
            Find answers to common questions about using BenefitPlate
          </p>
        </div>

        {/* Why Different */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Why This Is Different</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h3 className="font-semibold text-lg mb-2">vs. 211 Services</h3>
              <p className="text-gray-600">
                211 is a comprehensive directory, which is excellent for discovering resources.
                However, it can be overwhelming to navigate. BenefitPlate helps you narrow down
                programs that fit your specific situation through guided eligibility screening
                and personalized results.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">vs. State and Medicaid Websites</h3>
              <p className="text-gray-600">
                State and Medicaid websites are authoritative sources but can be difficult to
                navigate and are often written in complex policy language. BenefitPlate translates
                these programs into a guided, user-friendly flow with clear next steps.
              </p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-gray-700">
                <strong>Our approach:</strong> ZIP-based filtering + short guided questionnaire +
                deterministic rule-based matching + checklist and next steps + ability to save
                results for later reference.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* FAQ */}
        <Card>
          <CardHeader>
            <CardTitle>Frequently Asked Questions</CardTitle>
          </CardHeader>
          <CardContent>
            <Accordion type="single" collapsible className="w-full">
              <AccordionItem value="item-1">
                <AccordionTrigger>What is BenefitPlate?</AccordionTrigger>
                <AccordionContent>
                  BenefitPlate is a tool that helps you discover Food is Medicine and food support
                  programs you may qualify for based on your ZIP code and a short questionnaire.
                  We provide clear next steps and a downloadable checklist.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-2">
                <AccordionTrigger>Do I need to create an account?</AccordionTrigger>
                <AccordionContent>
                  No, you can browse programs and take the eligibility questionnaire without an
                  account. However, if you want to save your results or download a PDF checklist,
                  you'll need to sign in with your Google account.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-3">
                <AccordionTrigger>Is this a government website?</AccordionTrigger>
                <AccordionContent>
                  No, BenefitPlate is not a government agency. We provide informational guidance
                  to help you find programs. Eligibility varies by program and must be verified
                  by the program provider.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-4">
                <AccordionTrigger>How accurate are the eligibility results?</AccordionTrigger>
                <AccordionContent>
                  Our eligibility screening uses deterministic rules based on official program
                  requirements. However, final eligibility must be confirmed by the program
                  provider. We categorize programs as "Likely Eligible," "Possibly Eligible,"
                  or "Community Programs" to give you a sense of your match.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-5">
                <AccordionTrigger>What information do you collect?</AccordionTrigger>
                <AccordionContent>
                  We collect only the information you provide in the questionnaire (ZIP code,
                  enrollment status, household size, income band, age range, pregnancy status,
                  and health condition categories). We do NOT collect exact income amounts,
                  specific diagnoses, or any medical records.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-6">
                <AccordionTrigger>How do I apply for a program?</AccordionTrigger>
                <AccordionContent>
                  Each program card includes application information, such as website links and
                  phone numbers. You'll need to contact the program directly using the provided
                  information. We also provide a checklist of required documents to help you prepare.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-7">
                <AccordionTrigger>What if my ZIP code isn't found?</AccordionTrigger>
                <AccordionContent>
                  We currently have coverage for major metropolitan areas. If your ZIP code isn't
                  found, you can still browse all programs or try checking eligibility with a
                  nearby ZIP code in your county.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-8">
                <AccordionTrigger>How often is program information updated?</AccordionTrigger>
                <AccordionContent>
                  We verify program information regularly. Each program listing shows the last
                  verification date. If you find outdated information, please contact the program
                  directly for the most current details.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card>

        {/* Disclaimer */}
        <Card className="mt-6 bg-yellow-50 border-yellow-200">
          <CardContent className="py-4">
            <p className="text-sm text-gray-700">
              <strong>Important:</strong> This tool provides informational guidance and is not a
              government agency. Eligibility varies by program and may require verification by the
              program provider. We do not provide medical advice. For official information, please
              contact the programs directly.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default HelpPage;
