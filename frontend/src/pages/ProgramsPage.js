import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Search, ExternalLink, Phone, Loader2 } from 'lucide-react';
import { programsAPI } from '@/utils/api';
import { toast } from 'sonner';

const BENEFIT_TYPES = [
  { value: 'all', label: 'All Types' },
  { value: 'produce_rx', label: 'Produce Rx' },
  { value: 'mtg', label: 'Medically Tailored Groceries' },
  { value: 'mtm', label: 'Medically Tailored Meals' },
  { value: 'pantry', label: 'Food Pantry' },
  { value: 'snap_support', label: 'SNAP Support' },
  { value: 'nutrition_coaching', label: 'Nutrition Coaching' },
];

const ProgramsPage = () => {
  const navigate = useNavigate();
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [benefitTypeFilter, setBenefitTypeFilter] = useState('all');
  const [stateFilter, setStateFilter] = useState('all');

  useEffect(() => {
    loadPrograms();
  }, [benefitTypeFilter, stateFilter]);

  const loadPrograms = async () => {
    setLoading(true);
    try {
      const params = {};
      if (benefitTypeFilter !== 'all') params.benefit_type = benefitTypeFilter;
      if (stateFilter !== 'all') params.state = stateFilter;

      const response = await programsAPI.list(params);
      setPrograms(response.data);
    } catch (error) {
      console.error('Failed to load programs:', error);
      toast.error('Failed to load programs');
    } finally {
      setLoading(false);
    }
  };

  const filteredPrograms = programs.filter(program =>
    program.program_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    program.county?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    program.state?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2" data-testid="programs-page">
            Browse Programs
          </h1>
          <p className="text-gray-600">
            Explore food and nutrition assistance programs
          </p>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Search</label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search programs..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">Benefit Type</label>
                <Select value={benefitTypeFilter} onValueChange={setBenefitTypeFilter}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {BENEFIT_TYPES.map(type => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">State</label>
                <Select value={stateFilter} onValueChange={setStateFilter}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All States</SelectItem>
                    <SelectItem value="California">California</SelectItem>
                    <SelectItem value="New York">New York</SelectItem>
                    <SelectItem value="Texas">Texas</SelectItem>
                    <SelectItem value="Massachusetts">Massachusetts</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          </div>
        ) : filteredPrograms.length > 0 ? (
          <div className="grid gap-4">
            {filteredPrograms.map(program => (
              <Card key={program.program_id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-2">{program.program_name}</CardTitle>
                      <div className="flex flex-wrap gap-2 mb-2">
                        <Badge variant="secondary">
                          {program.benefit_type.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                        </Badge>
                        {program.geo_scope === 'national' ? (
                          <Badge variant="outline">National</Badge>
                        ) : (
                          <Badge variant="outline">
                            {program.county || program.state}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {program.how_to_apply_url && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => window.open(program.how_to_apply_url, '_blank')}
                      >
                        <ExternalLink className="h-4 w-4 mr-2" />
                        Website
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
                      variant="default"
                      size="sm"
                      onClick={() => navigate(`/programs/${program.program_id}`)}
                    >
                      View Details
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center text-gray-600">
              <p>No programs found matching your criteria.</p>
              <Button
                variant="link"
                onClick={() => {
                  setSearchTerm('');
                  setBenefitTypeFilter('all');
                  setStateFilter('all');
                }}
                className="mt-2"
              >
                Clear filters
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ProgramsPage;
