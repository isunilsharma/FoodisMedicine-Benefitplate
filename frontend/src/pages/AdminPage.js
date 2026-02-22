import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Plus, Edit, Trash2, Loader2, AlertCircle } from 'lucide-react';
import { adminAPI } from '@/utils/api';
import { toast } from 'sonner';

const BENEFIT_TYPES = ['produce_rx', 'mtg', 'mtm', 'pantry', 'snap_support', 'nutrition_coaching', 'other'];
const GEO_SCOPES = ['national', 'state', 'county', 'city', 'zip'];
const STATUSES = ['active', 'paused', 'deprecated'];

const AdminPage = () => {
  const [programs, setPrograms] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [editingProgram, setEditingProgram] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [formData, setFormData] = useState({
    program_name: '',
    benefit_type: 'produce_rx',
    geo_scope: 'state',
    state: '',
    county: '',
    how_to_apply_url: '',
    contact_phone: '',
    source_urls: '',
    eligibility_conditions_json: '{}',
    document_checklist_json: '{"required": [], "optional": []}',
    referral_required: false,
    requires_medicaid: false,
    requires_snap: false,
    income_fpl_bands_allowed: '',
    notes: '',
  });

  useEffect(() => {
    loadPrograms();
    loadAnalytics();
  }, []);

  const loadPrograms = async () => {
    setLoading(true);
    try {
      const response = await adminAPI.listPrograms();
      setPrograms(response.data);
    } catch (error) {
      console.error('Failed to load programs:', error);
      toast.error('Failed to load programs');
    } finally {
      setLoading(false);
    }
  };

  const loadAnalytics = async () => {
    setAnalyticsLoading(true);
    try {
      const response = await adminAPI.getAnalytics(30);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setAnalyticsLoading(false);
    }
  };

  const handleOpenDialog = (program = null) => {
    if (program) {
      setEditingProgram(program);
      setFormData({
        program_name: program.program_name,
        benefit_type: program.benefit_type,
        geo_scope: program.geo_scope,
        state: program.state || '',
        county: program.county || '',
        how_to_apply_url: program.how_to_apply_url || '',
        contact_phone: program.contact_phone || '',
        source_urls: program.source_urls?.join('\n') || '',
        eligibility_conditions_json: '{}',
        document_checklist_json: '{"required": [], "optional": []}',
        referral_required: false,
        requires_medicaid: false,
        requires_snap: false,
        income_fpl_bands_allowed: '',
        notes: '',
      });
    } else {
      setEditingProgram(null);
      setFormData({
        program_name: '',
        benefit_type: 'produce_rx',
        geo_scope: 'state',
        state: '',
        county: '',
        how_to_apply_url: '',
        contact_phone: '',
        source_urls: '',
        eligibility_conditions_json: '{}',
        document_checklist_json: '{"required": [], "optional": []}',
        referral_required: false,
        requires_medicaid: false,
        requires_snap: false,
        income_fpl_bands_allowed: '',
        notes: '',
      });
    }
    setIsDialogOpen(true);
  };

  const handleSaveProgram = async () => {
    try {
      // Validate JSON fields
      let eligibilityJson, checklistJson;
      try {
        eligibilityJson = JSON.parse(formData.eligibility_conditions_json);
        checklistJson = JSON.parse(formData.document_checklist_json);
      } catch (e) {
        toast.error('Invalid JSON in eligibility conditions or document checklist');
        return;
      }

      const programData = {
        program_name: formData.program_name,
        benefit_type: formData.benefit_type,
        geo_scope: formData.geo_scope,
        state: formData.state || null,
        county: formData.county || null,
        how_to_apply_url: formData.how_to_apply_url || null,
        contact_phone: formData.contact_phone || null,
        source_urls: formData.source_urls.split('\n').filter(u => u.trim()),
        eligibility_conditions_json: eligibilityJson,
        document_checklist_json: checklistJson,
        referral_required: formData.referral_required,
        requires_medicaid: formData.requires_medicaid,
        requires_snap: formData.requires_snap,
        income_fpl_bands_allowed: formData.income_fpl_bands_allowed.split(',').map(s => s.trim()).filter(s => s),
        notes: formData.notes || null,
      };

      if (editingProgram) {
        await adminAPI.updateProgram(editingProgram.program_id, programData);
        toast.success('Program updated successfully');
      } else {
        await adminAPI.createProgram(programData);
        toast.success('Program created successfully');
      }

      setIsDialogOpen(false);
      loadPrograms();
    } catch (error) {
      console.error('Save error:', error);
      toast.error('Failed to save program');
    }
  };

  const handleDeleteProgram = async (programId) => {
    if (!window.confirm('Are you sure you want to delete this program?')) return;

    try {
      await adminAPI.deleteProgram(programId);
      toast.success('Program deleted successfully');
      loadPrograms();
    } catch (error) {
      console.error('Delete error:', error);
      toast.error('Failed to delete program');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2" data-testid="admin-page">
              Admin Console
            </h1>
            <p className="text-gray-600">Manage programs and view analytics</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => handleOpenDialog()} data-testid="create-program-btn">
                <Plus className="h-4 w-4 mr-2" />
                Create Program
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>
                  {editingProgram ? 'Edit Program' : 'Create New Program'}
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div>
                  <Label>Program Name *</Label>
                  <Input
                    value={formData.program_name}
                    onChange={(e) => setFormData({ ...formData, program_name: e.target.value })}
                    placeholder="e.g., California Fresh Produce Rx"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Benefit Type *</Label>
                    <Select
                      value={formData.benefit_type}
                      onValueChange={(v) => setFormData({ ...formData, benefit_type: v })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {BENEFIT_TYPES.map(type => (
                          <SelectItem key={type} value={type}>
                            {type.replace('_', ' ').toUpperCase()}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Geographic Scope *</Label>
                    <Select
                      value={formData.geo_scope}
                      onValueChange={(v) => setFormData({ ...formData, geo_scope: v })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {GEO_SCOPES.map(scope => (
                          <SelectItem key={scope} value={scope}>
                            {scope.toUpperCase()}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>State</Label>
                    <Input
                      value={formData.state}
                      onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                      placeholder="e.g., California"
                    />
                  </div>
                  <div>
                    <Label>County</Label>
                    <Input
                      value={formData.county}
                      onChange={(e) => setFormData({ ...formData, county: e.target.value })}
                      placeholder="e.g., Los Angeles County"
                    />
                  </div>
                </div>

                <div>
                  <Label>Application URL</Label>
                  <Input
                    value={formData.how_to_apply_url}
                    onChange={(e) => setFormData({ ...formData, how_to_apply_url: e.target.value })}
                    placeholder="https://..."
                  />
                </div>

                <div>
                  <Label>Contact Phone</Label>
                  <Input
                    value={formData.contact_phone}
                    onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                    placeholder="1-800-555-0100"
                  />
                </div>

                <div>
                  <Label>Source URLs (one per line)</Label>
                  <Textarea
                    value={formData.source_urls}
                    onChange={(e) => setFormData({ ...formData, source_urls: e.target.value })}
                    placeholder="https://source1.com\nhttps://source2.com"
                    rows={3}
                  />
                </div>

                <div>
                  <Label>Eligibility Conditions (JSON)</Label>
                  <Textarea
                    value={formData.eligibility_conditions_json}
                    onChange={(e) => setFormData({ ...formData, eligibility_conditions_json: e.target.value })}
                    placeholder='{}'
                    rows={4}
                    className="font-mono text-sm"
                  />
                </div>

                <div>
                  <Label>Document Checklist (JSON)</Label>
                  <Textarea
                    value={formData.document_checklist_json}
                    onChange={(e) => setFormData({ ...formData, document_checklist_json: e.target.value })}
                    placeholder='{"required": ["ID", "Proof of income"], "optional": []}'
                    rows={4}
                    className="font-mono text-sm"
                  />
                </div>

                <div>
                  <Label>Income FPL Bands (comma-separated)</Label>
                  <Input
                    value={formData.income_fpl_bands_allowed}
                    onChange={(e) => setFormData({ ...formData, income_fpl_bands_allowed: e.target.value })}
                    placeholder="Under 100% FPL, 100-138% FPL"
                  />
                </div>

                <div className="flex gap-4">
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.referral_required}
                      onChange={(e) => setFormData({ ...formData, referral_required: e.target.checked })}
                    />
                    <span className="text-sm">Referral Required</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.requires_medicaid}
                      onChange={(e) => setFormData({ ...formData, requires_medicaid: e.target.checked })}
                    />
                    <span className="text-sm">Requires Medicaid</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.requires_snap}
                      onChange={(e) => setFormData({ ...formData, requires_snap: e.target.checked })}
                    />
                    <span className="text-sm">Requires SNAP</span>
                  </label>
                </div>

                <div>
                  <Label>Notes</Label>
                  <Textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows={3}
                  />
                </div>

                <div className="flex justify-end gap-2 pt-4">
                  <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleSaveProgram}>
                    {editingProgram ? 'Update' : 'Create'} Program
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          </div>
        ) : (
          <Tabs defaultValue="programs" className="space-y-4">
            <TabsList>
              <TabsTrigger value="programs">Programs ({programs.length})</TabsTrigger>
              <TabsTrigger value="analytics">Analytics</TabsTrigger>
            </TabsList>

            <TabsContent value="programs" className="space-y-4">
              {programs.map(program => (
                <Card key={program.program_id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-xl mb-2">{program.program_name}</CardTitle>
                        <div className="flex flex-wrap gap-2">
                          <Badge variant="secondary">{program.benefit_type}</Badge>
                          <Badge variant="outline">{program.geo_scope}</Badge>
                          {program.state && <Badge variant="outline">{program.state}</Badge>}
                          <Badge variant={program.status === 'active' ? 'default' : 'secondary'}>
                            {program.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleOpenDialog(program)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeleteProgram(program.program_id)}
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">
                      Last verified: {new Date(program.last_verified_at).toLocaleDateString()}
                    </p>
                  </CardContent>
                </Card>
              ))}

              {programs.length === 0 && (
                <Card>
                  <CardContent className="py-12 text-center text-gray-600">
                    <AlertCircle className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                    <p>No programs found. Create your first program to get started.</p>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            <TabsContent value="analytics">
              {analyticsLoading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                </div>
              ) : analytics ? (
                <div className="space-y-4">
                  {/* Analytics Summary Cards */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <Card>
                      <CardHeader className="pb-2">
                        <p className="text-sm text-gray-600">Total Events</p>
                      </CardHeader>
                      <CardContent>
                        <p className="text-3xl font-bold">{analytics.total_events}</p>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardHeader className="pb-2">
                        <p className="text-sm text-gray-600">ZIP Searches</p>
                      </CardHeader>
                      <CardContent>
                        <p className="text-3xl font-bold">{analytics.zip_submitted}</p>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardHeader className="pb-2">
                        <p className="text-sm text-gray-600">Completed</p>
                      </CardHeader>
                      <CardContent>
                        <p className="text-3xl font-bold">{analytics.questionnaire_completed}</p>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardHeader className="pb-2">
                        <p className="text-sm text-gray-600">Saved Results</p>
                      </CardHeader>
                      <CardContent>
                        <p className="text-3xl font-bold">{analytics.result_saved}</p>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Event Breakdown */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Event Breakdown (Last 30 Days)</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Programs Shown</span>
                          <Badge>{analytics.programs_shown}</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Program Details Clicked</span>
                          <Badge>{analytics.program_detail_clicked}</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Checklists Downloaded</span>
                          <Badge>{analytics.checklist_downloaded}</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Unique Users</span>
                          <Badge>{analytics.unique_users}</Badge>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Recent Events */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2 max-h-96 overflow-y-auto">
                        {analytics.recent_events.map((event, idx) => (
                          <div key={idx} className="flex justify-between items-center text-sm border-b pb-2">
                            <span className="font-medium">{event.event_type.replace(/_/g, ' ')}</span>
                            <span className="text-gray-500">{new Date(event.timestamp).toLocaleString()}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <Card>
                  <CardContent className="py-12 text-center text-gray-600">
                    <p>No analytics data available</p>
                  </CardContent>
                </Card>
              )}
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  );
};

export default AdminPage;
