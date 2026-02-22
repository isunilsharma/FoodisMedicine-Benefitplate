import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { MapPin, FileText, CheckCircle, ArrowRight } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20" data-testid="landing-page">
        <div className="text-center">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Find food and nutrition benefits you may qualify for
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Answer a few questions. Get programs in your ZIP code, eligibility guidance,
            and a simple checklist of what to do next.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              onClick={() => navigate('/check-eligibility')}
              size="lg"
              className="text-lg px-8 py-6"
              data-testid="check-eligibility-btn"
            >
              Check Eligibility
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button
              onClick={() => navigate('/programs')}
              variant="outline"
              size="lg"
              className="text-lg px-8 py-6"
              data-testid="browse-programs-btn"
            >
              Browse Programs
            </Button>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <MapPin className="h-6 w-6 text-blue-600" />
              </div>
              <CardTitle>ZIP-specific results</CardTitle>
              <CardDescription className="mt-2">
                Programs available in your area, filtered by your ZIP code and county
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-green-600" />
              </div>
              <CardTitle>Simple eligibility guidance</CardTitle>
              <CardDescription className="mt-2">
                Clear explanations of why you match programs and what you need to apply
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <CheckCircle className="h-6 w-6 text-purple-600" />
              </div>
              <CardTitle>Downloadable checklist</CardTitle>
              <CardDescription className="mt-2">
                Get a PDF with all required documents and next steps for each program
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* Why This Is Different */}
        <div className="mt-20 bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
            Why this is different
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">vs. 211 Services</h3>
              <p className="text-gray-600">
                211 is a comprehensive directory, which is great for discovery. We help you narrow down
                what fits your specific situation with guided eligibility screening and personalized results.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">vs. State Websites</h3>
              <p className="text-gray-600">
                State and Medicaid sites are authoritative but can be hard to navigate and are often
                written in policy language. We translate them into a guided flow with clear next steps.
              </p>
            </div>
          </div>
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-700">
              <strong>Our approach:</strong> ZIP-based filtering + short guided questionnaire +
              deterministic rule-based matching + checklist and next steps + saved results and reminders
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
