import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, ArrowRight, Loader2 } from 'lucide-react';
import { geographyAPI, eligibilityAPI } from '@/utils/api';
import { toast } from 'sonner';

const HEALTH_CONDITIONS = [
  'Diabetes',
  'Heart disease',
  'Hypertension',
  'Kidney disease',
  'Pregnancy/postpartum nutrition',
  'None / Prefer not to say',
];

const CheckEligibilityPage = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [zipLookupData, setZipLookupData] = useState(null);

  const [formData, setFormData] = useState({
    zip_code: '',
    enrolled_medicaid: '',
    enrolled_snap: '',
    household_size: 1,
    income_band: '',
    age_range: '',
    pregnancy: '',
    health_conditions: [],
    has_case_manager: '',
  });

  const totalSteps = 9;
  const progress = ((step + 1) / totalSteps) * 100;

  const handleNext = async () => {
    // Validate current step
    if (step === 0 && !formData.zip_code) {
      toast.error('Please enter your ZIP code');
      return;
    }

    // Lookup ZIP on first step
    if (step === 0) {
      setLoading(true);
      try {
        const response = await geographyAPI.lookupZip(formData.zip_code);
        setZipLookupData(response.data);
        
        // Check if California
        if (response.data.state_code !== 'CA') {
          toast.error(
            'Our service is currently available in California only. We\'re working to expand coverage to your area.',
            { duration: 6000 }
          );
          setLoading(false);
          return; // Block progression to next step
        }
        
        toast.success(`Found: ${response.data.county}, ${response.data.state}`);
        setStep(step + 1);
      } catch (error) {
        toast.error('ZIP code not found. Please check and try again.');
      } finally {
        setLoading(false);
      }
      return;
    }

    if (step < totalSteps - 1) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    console.log('handleSubmit called', { zipLookupData, formData });
    
    // Validate ZIP lookup happened
    if (!zipLookupData) {
      toast.error('Please complete ZIP code lookup first');
      return;
    }

    // Validate required fields
    if (!formData.enrolled_medicaid || !formData.enrolled_snap || !formData.income_band || 
        !formData.age_range || !formData.pregnancy || !formData.has_case_manager) {
      toast.error('Please answer all questions');
      console.log('Missing fields:', {
        medicaid: formData.enrolled_medicaid,
        snap: formData.enrolled_snap,
        income: formData.income_band,
        age: formData.age_range,
        pregnancy: formData.pregnancy,
        case_manager: formData.has_case_manager
      });
      return;
    }

    setLoading(true);
    try {
      console.log('Calling eligibility API...');
      const response = await eligibilityAPI.evaluate(formData.zip_code, {
        enrolled_medicaid: formData.enrolled_medicaid,
        enrolled_snap: formData.enrolled_snap,
        household_size: formData.household_size,
        income_band: formData.income_band,
        age_range: formData.age_range,
        pregnancy: formData.pregnancy,
        health_conditions: formData.health_conditions,
        has_case_manager: formData.has_case_manager,
      });

      console.log('Eligibility response:', response.data);
      
      // Navigate to results with data
      navigate('/results', { state: { results: response.data, formData, zipLookupData } });
    } catch (error) {
      console.error('Evaluation error:', error);
      toast.error(`Failed to evaluate eligibility: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const updateFormData = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const toggleHealthCondition = (condition) => {
    const current = formData.health_conditions;
    if (current.includes(condition)) {
      updateFormData('health_conditions', current.filter(c => c !== condition));
    } else {
      updateFormData('health_conditions', [...current, condition]);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <div className="space-y-4">
            <Label htmlFor="zip_code" className="text-lg">What is your ZIP code?</Label>
            <Input
              id="zip_code"
              type="text"
              placeholder="Enter ZIP code"
              value={formData.zip_code}
              onChange={(e) => updateFormData('zip_code', e.target.value)}
              maxLength={5}
              data-testid="zip-input"
              className="text-lg"
            />
            {zipLookupData && (
              <p className="text-sm text-green-600">
                ✓ {zipLookupData.county}, {zipLookupData.state}
              </p>
            )}
          </div>
        );

      case 1:
        return (
          <div className="space-y-4">
            <Label className="text-lg">Are you currently enrolled in Medicaid?</Label>
            <RadioGroup value={formData.enrolled_medicaid} onValueChange={(v) => updateFormData('enrolled_medicaid', v)}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Yes" id="medicaid-yes" />
                <Label htmlFor="medicaid-yes">Yes</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="No" id="medicaid-no" />
                <Label htmlFor="medicaid-no">No</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Not sure" id="medicaid-unsure" />
                <Label htmlFor="medicaid-unsure">Not sure</Label>
              </div>
            </RadioGroup>
          </div>
        );

      case 2:
        return (
          <div className="space-y-4">
            <Label className="text-lg">Are you enrolled in SNAP (food stamps)?</Label>
            <RadioGroup value={formData.enrolled_snap} onValueChange={(v) => updateFormData('enrolled_snap', v)}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Yes" id="snap-yes" />
                <Label htmlFor="snap-yes">Yes</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="No" id="snap-no" />
                <Label htmlFor="snap-no">No</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Not sure" id="snap-unsure" />
                <Label htmlFor="snap-unsure">Not sure</Label>
              </div>
            </RadioGroup>
          </div>
        );

      case 3:
        return (
          <div className="space-y-4">
            <Label htmlFor="household_size" className="text-lg">How many people are in your household?</Label>
            <Input
              id="household_size"
              type="number"
              min={1}
              max={15}
              value={formData.household_size}
              onChange={(e) => updateFormData('household_size', parseInt(e.target.value))}
              className="text-lg"
            />
          </div>
        );

      case 4:
        return (
          <div className="space-y-4">
            <Label className="text-lg">What is your household income range? (Compared to Federal Poverty Level)</Label>
            <RadioGroup value={formData.income_band} onValueChange={(v) => updateFormData('income_band', v)}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Under 100% FPL" id="income-1" />
                <Label htmlFor="income-1">Under 100% FPL</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="100-138% FPL" id="income-2" />
                <Label htmlFor="income-2">100-138% FPL</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="139-200% FPL" id="income-3" />
                <Label htmlFor="income-3">139-200% FPL</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="201-300% FPL" id="income-4" />
                <Label htmlFor="income-4">201-300% FPL</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Over 300% FPL" id="income-5" />
                <Label htmlFor="income-5">Over 300% FPL</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Not sure" id="income-unsure" />
                <Label htmlFor="income-unsure">Not sure</Label>
              </div>
            </RadioGroup>
          </div>
        );

      case 5:
        return (
          <div className="space-y-4">
            <Label className="text-lg">What is your age range?</Label>
            <RadioGroup value={formData.age_range} onValueChange={(v) => updateFormData('age_range', v)}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Under 18" id="age-1" />
                <Label htmlFor="age-1">Under 18</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="18-59" id="age-2" />
                <Label htmlFor="age-2">18-59</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="60+" id="age-3" />
                <Label htmlFor="age-3">60+</Label>
              </div>
            </RadioGroup>
          </div>
        );

      case 6:
        return (
          <div className="space-y-4">
            <Label className="text-lg">Are you currently pregnant or postpartum?</Label>
            <RadioGroup value={formData.pregnancy} onValueChange={(v) => updateFormData('pregnancy', v)}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Yes" id="pregnancy-yes" />
                <Label htmlFor="pregnancy-yes">Yes</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="No" id="pregnancy-no" />
                <Label htmlFor="pregnancy-no">No</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Prefer not to say" id="pregnancy-prefer" />
                <Label htmlFor="pregnancy-prefer">Prefer not to say</Label>
              </div>
            </RadioGroup>
          </div>
        );

      case 7:
        return (
          <div className="space-y-4">
            <Label className="text-lg">Do you have any of these health conditions? (Optional, select all that apply)</Label>
            <div className="space-y-3">
              {HEALTH_CONDITIONS.map((condition) => (
                <div key={condition} className="flex items-center space-x-2">
                  <Checkbox
                    id={`condition-${condition}`}
                    checked={formData.health_conditions.includes(condition)}
                    onCheckedChange={() => toggleHealthCondition(condition)}
                  />
                  <Label htmlFor={`condition-${condition}`} className="font-normal">
                    {condition}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        );

      case 8:
        return (
          <div className="space-y-4">
            <Label className="text-lg">Do you have a case manager or clinic you work with?</Label>
            <RadioGroup value={formData.has_case_manager} onValueChange={(v) => updateFormData('has_case_manager', v)}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Yes" id="case-yes" />
                <Label htmlFor="case-yes">Yes</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="No" id="case-no" />
                <Label htmlFor="case-no">No</Label>
              </div>
            </RadioGroup>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Check Your Eligibility</CardTitle>
            <div className="mt-4">
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span>Question {step + 1} of {totalSteps}</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {renderStep()}

            <div className="flex justify-between pt-6">
              <Button
                onClick={handleBack}
                variant="outline"
                disabled={step === 0 || loading}
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </Button>

              {step < totalSteps - 1 ? (
                <Button onClick={handleNext} disabled={loading}>
                  {loading ? (
                    <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Loading...</>
                  ) : (
                    <>Next <ArrowRight className="ml-2 h-4 w-4" /></>
                  )}
                </Button>
              ) : (
                <Button onClick={handleSubmit} disabled={loading} data-testid="evaluate-btn">
                  {loading ? (
                    <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Evaluating...</>
                  ) : (
                    'Find Programs'
                  )}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CheckEligibilityPage;
