import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Calendar, MapPin, Loader2 } from 'lucide-react';
import { userAPI } from '@/utils/api';
import { toast } from 'sonner';

const DashboardPage = () => {
  const navigate = useNavigate();
  const [savedResults, setSavedResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSavedResults();
  }, []);

  const loadSavedResults = async () => {
    setLoading(true);
    try {
      const response = await userAPI.getSavedResults();
      setSavedResults(response.data);
    } catch (error) {
      console.error('Failed to load saved results:', error);
      toast.error('Failed to load saved results');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2" data-testid="dashboard-page">
            My Saved Results
          </h1>
          <p className="text-gray-600">
            View your previously saved eligibility screenings
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          </div>
        ) : savedResults.length > 0 ? (
          <div className="space-y-4">
            {savedResults.map(result => (
              <Card key={result.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-xl mb-2">
                        <MapPin className="inline h-5 w-5 mr-2" />
                        {result.county}, {result.state}
                      </CardTitle>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Calendar className="h-4 w-4" />
                        <span>
                          Saved on {new Date(result.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <Badge variant="outline">ZIP: {result.zip_code}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-3">
                    {result.matched_program_ids.length} programs matched
                  </p>
                  <Button
                    size="sm"
                    onClick={() => navigate('/check-eligibility')}
                  >
                    Run New Search
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-600 mb-4">You haven't saved any results yet.</p>
              <Button onClick={() => navigate('/check-eligibility')}>
                Check Your Eligibility
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
