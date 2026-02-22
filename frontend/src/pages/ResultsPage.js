import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { CheckCircle, AlertCircle, Info, Download, Save, ExternalLink, Phone } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { userAPI } from '@/utils/api';
import { toast } from 'sonner';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, login } = useAuth();
  const [saving, setSaving] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const { results, formData } = location.state || {};

  if (!results) {
    navigate('/');
    return null;
  }

  const allPrograms = [
    ...results.likely_eligible,
    ...results.possibly_eligible,
    ...results.community,
  ];

  const handleSave = async () => {
    if (!isAuthenticated) {
      toast.error('Please sign in to save your results');
      login();
      return;
    }

    setSaving(true);
    try {
      await userAPI.saveResult({
        zip_code: results.zip_code,
        county: results.county,
        state: results.state,
        answers: formData,
        matched_program_ids: allPrograms.map(p => p.program_id),
      });
      toast.success('Results saved successfully!');
    } catch (error) {
      console.error('Save error:', error);
      toast.error('Failed to save results');
    } finally {
      setSaving(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!isAuthenticated) {
      toast.error('Please sign in to download checklist');
      login();
      return;
    }

    setDownloading(true);
    try {
      const response = await userAPI.generatePDF(
        allPrograms.map(p => p.program_id),
        results.zip_code,
        results.county,
        results.state
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `benefits_checklist_${new Date().toISOString().split('T')[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      toast.success('Checklist downloaded!');
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download checklist');
    } finally {
      setDownloading(false);
    }
  };

  const ProgramCard = ({ program, status }) => {
    const statusConfig = {
      likely: { icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-50', label: 'Likely Eligible' },
      possibly: { icon: AlertCircle, color: 'text-yellow-600', bg: 'bg-yellow-50', label: 'Possibly Eligible' },
      community: { icon: Info, color: 'text-blue-600', bg: 'bg-blue-50', label: 'Community Program' },
    };

    const config = statusConfig[status];
    const Icon = config.icon;

    return (
      <Card className="mb-4" data-testid={`program-card-${program.program_id}`}>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Icon className={`h-5 w-5 ${config.color}`} />
                <Badge variant="outline" className={config.color}>
                  {config.label}
                </Badge>
              </div>
              <CardTitle className="text-xl">{program.program_name}</CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                {program.benefit_type.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
              </p>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Why you match */}
          {program.why_you_match && (
            <div className={`p-3 rounded-lg ${config.bg}`}>
              <p className="text-sm font-semibold mb-1">Why you match:</p>
              <p className="text-sm">{program.why_you_match}</p>
            </div>
          )}

          {/* Matched conditions */}
          {program.matched_conditions && program.matched_conditions.length > 0 && (
            <div>
              <p className="text-sm font-semibold mb-2">Based on your answers:</p>
              <ul className="list-disc list-inside space-y-1">
                {program.matched_conditions.slice(0, 3).map((condition, idx) => (
                  <li key={idx} className="text-sm text-gray-700">{condition}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Required documents */}
          {program.document_checklist?.required && program.document_checklist.required.length > 0 && (
            <div>
              <p className="text-sm font-semibold mb-2">What you'll need:</p>
              <ul className="list-disc list-inside space-y-1">
                {program.document_checklist.required.map((doc, idx) => (
                  <li key={idx} className="text-sm text-gray-700">{doc}</li>
                ))}
              </ul>
            </div>
          )}

          {/* How to apply */}
          <div className="flex flex-wrap gap-2 pt-2">
            {program.how_to_apply_url && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.open(program.how_to_apply_url, '_blank')}
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                Apply Online
              </Button>
            )}
            {program.contact_phone && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.open(`tel:${program.contact_phone}`)}
              >
                <Phone className="h-4 w-4 mr-2" />
                {program.contact_phone}
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(`/programs/${program.program_id}`)}
            >
              View Details
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2" data-testid="results-page">
            Your Eligibility Results
          </h1>
          <p className="text-gray-600">
            {results.county}, {results.state} (ZIP: {results.zip_code})
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Found {allPrograms.length} programs that may be available to you
          </p>

          {/* Actions */}
          <div className="flex flex-wrap gap-3 mt-4">
            <Button onClick={handleSave} disabled={saving} data-testid="save-results-btn">
              <Save className="h-4 w-4 mr-2" />
              {saving ? 'Saving...' : 'Save Results'}
            </Button>
            <Button variant="outline" onClick={handleDownloadPDF} disabled={downloading}>
              <Download className="h-4 w-4 mr-2" />
              {downloading ? 'Generating...' : 'Download Checklist'}
            </Button>
          </div>
        </div>

        {/* Results Tabs */}
        <Tabs defaultValue="likely" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="likely">
              Likely Eligible ({results.likely_eligible.length})
            </TabsTrigger>
            <TabsTrigger value="possibly">
              Possibly Eligible ({results.possibly_eligible.length})
            </TabsTrigger>
            <TabsTrigger value="community">
              Community ({results.community.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="likely">
            {results.likely_eligible.length > 0 ? (
              results.likely_eligible.map(program => (
                <ProgramCard key={program.program_id} program={program} status="likely" />
              ))
            ) : (
              <Card>
                <CardContent className="py-8 text-center text-gray-600">
                  No programs found in this category. Check other tabs for more options.
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="possibly">
            {results.possibly_eligible.length > 0 ? (
              results.possibly_eligible.map(program => (
                <ProgramCard key={program.program_id} program={program} status="possibly" />
              ))
            ) : (
              <Card>
                <CardContent className="py-8 text-center text-gray-600">
                  No programs found in this category.
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="community">
            {results.community.length > 0 ? (
              results.community.map(program => (
                <ProgramCard key={program.program_id} program={program} status="community" />
              ))
            ) : (
              <Card>
                <CardContent className="py-8 text-center text-gray-600">
                  No community programs found.
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>

        {/* Info Box */}
        <Card className="mt-6 bg-blue-50 border-blue-200">
          <CardContent className="py-4">
            <p className="text-sm text-gray-700">
              <strong>Next steps:</strong> Review the programs above, gather required documents, and apply using the provided links or phone numbers.
              If you need help, contact the program directly or speak with your case manager.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ResultsPage;
