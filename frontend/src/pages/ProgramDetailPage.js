import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, ExternalLink, Phone, Calendar, Loader2 } from 'lucide-react';
import { programsAPI } from '@/utils/api';
import { toast } from 'sonner';

const ProgramDetailPage = () => {
  const { programId } = useParams();
  const navigate = useNavigate();
  const [program, setProgram] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgram();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [programId]);

  const loadProgram = async () => {
    setLoading(true);
    try {
      const response = await programsAPI.getById(programId);
      setProgram(response.data);
    } catch (error) {
      console.error('Failed to load program:', error);
      toast.error('Program not found');
      navigate('/programs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!program) return null;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <Button
          variant="ghost"
          onClick={() => navigate(-1)}
          className="mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>

        <Card>
          <CardHeader>
            <div className="flex flex-wrap gap-2 mb-3">
              <Badge variant="secondary">
                {program.benefit_type.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
              </Badge>
              {program.geo_scope === 'national' ? (
                <Badge variant="outline">National Program</Badge>
              ) : (
                <Badge variant="outline">
                  {program.county || program.state}
                </Badge>
              )}
              <Badge variant={program.status === 'active' ? 'default' : 'secondary'}>
                {program.status}
              </Badge>
            </div>
            <CardTitle className="text-3xl">{program.program_name}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Program Info */}
            <div>
              <h3 className="font-semibold text-lg mb-2">Program Information</h3>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm text-gray-600">Benefit Type</dt>
                  <dd className="font-medium">
                    {program.benefit_type.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-600">Geographic Scope</dt>
                  <dd className="font-medium capitalize">{program.geo_scope}</dd>
                </div>
                {program.state && (
                  <div>
                    <dt className="text-sm text-gray-600">State</dt>
                    <dd className="font-medium">{program.state}</dd>
                  </div>
                )}
                {program.county && (
                  <div>
                    <dt className="text-sm text-gray-600">County</dt>
                    <dd className="font-medium">{program.county}</dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Last Verified */}
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Calendar className="h-4 w-4" />
              <span>
                Last verified: {new Date(program.last_verified_at).toLocaleDateString()}
              </span>
            </div>

            {/* Contact Information */}
            <div>
              <h3 className="font-semibold text-lg mb-3">How to Apply</h3>
              <div className="flex flex-wrap gap-3">
                {program.how_to_apply_url && (
                  <Button
                    onClick={() => window.open(program.how_to_apply_url, '_blank')}
                  >
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Apply Online
                  </Button>
                )}
                {program.contact_phone && (
                  <Button
                    variant="outline"
                    onClick={() => window.open(`tel:${program.contact_phone}`)}
                  >
                    <Phone className="h-4 w-4 mr-2" />
                    {program.contact_phone}
                  </Button>
                )}
              </div>
            </div>

            {/* Source URLs */}
            {program.source_urls && program.source_urls.length > 0 && (
              <div>
                <h3 className="font-semibold text-lg mb-2">Official Sources</h3>
                <ul className="space-y-2">
                  {program.source_urls.map((url, idx) => (
                    <li key={idx}>
                      <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm flex items-center gap-2"
                      >
                        <ExternalLink className="h-3 w-3" />
                        {url}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Check Eligibility CTA */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
              <p className="text-sm text-gray-700 mb-3">
                Want to see if you're eligible for this program?
              </p>
              <Button onClick={() => navigate('/check-eligibility')}>
                Check Your Eligibility
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProgramDetailPage;
