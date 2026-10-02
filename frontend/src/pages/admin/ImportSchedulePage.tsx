import { useState } from 'react';
import { useAuth } from '../../auth/AuthContext';

export default function ImportSchedulePage() {
  const { session } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<any>(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const headers = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session?.access_token}`,
  });

  const handleParse = async () => {
    if (!file || !session) return;
    setLoading(true);
    setMessage('');
    const text = await file.text();
    const res = await fetch('/api/schedules/import/parse', {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify({ content: text }),
    });
    setLoading(false);
    if (res.ok) {
      setPreview(await res.json());
    } else {
      const err = await res.json();
      setMessage('Error: ' + (err.detail || 'Failed to parse'));
    }
  };

  const handleConfirm = async () => {
    if (!preview?.parsed_rows || !session) return;
    setLoading(true);
    const res = await fetch('/api/schedules/import/confirm', {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify({ items: preview.parsed_rows }),
    });
    setLoading(false);
    if (res.ok) {
      const data = await res.json();
      setMessage(`Successfully imported ${data.inserted} schedules!`);
      setPreview(null);
      setFile(null);
    } else {
      const err = await res.json();
      setMessage('Error: ' + (err.detail || 'Import failed'));
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Import Schedule</h1>

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <p className="text-sm text-gray-500 mb-4">
          Upload a text file with format: <code className="bg-gray-100 px-1 rounded">DATE | EMPLOYEE_NAME | SHIFT_NAME</code> (one per line)
        </p>
        <div className="flex gap-4 items-center">
          <input
            type="file"
            accept=".txt,.csv"
            onChange={e => setFile(e.target.files?.[0] || null)}
            className="border border-gray-300 p-2 rounded-lg"
          />
          <button
            onClick={handleParse}
            disabled={!file || loading}
            className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800 disabled:opacity-50"
          >
            {loading ? 'Parsing...' : 'Parse File'}
          </button>
        </div>
      </div>

      {message && <div className="bg-blue-50 text-blue-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}

      {preview && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Preview ({preview.parsed_rows?.length || 0} rows)</h2>
          {preview.errors?.length > 0 && (
            <div className="bg-red-50 text-red-700 p-3 rounded mb-4">
              <p className="font-semibold mb-1">Errors:</p>
              {preview.errors.map((err: string, i: number) => <p key={i} className="text-sm">{err}</p>)}
            </div>
          )}
          {preview.parsed_rows?.length > 0 && (
            <>
              <div className="overflow-x-auto mb-4">
                <table className="w-full text-left">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="p-3 text-sm">Line</th>
                      <th className="p-3 text-sm">Date</th>
                      <th className="p-3 text-sm">Employee</th>
                      <th className="p-3 text-sm">Shift</th>
                    </tr>
                  </thead>
                  <tbody>
                    {preview.parsed_rows.map((row: any, i: number) => (
                      <tr key={i} className="border-t border-gray-100">
                        <td className="p-3 text-sm">{row.line}</td>
                        <td className="p-3 text-sm">{row.date}</td>
                        <td className="p-3 text-sm">{row.employee_name}</td>
                        <td className="p-3 text-sm">{row.shift_name}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <button
                onClick={handleConfirm}
                disabled={loading}
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Importing...' : 'Confirm Import'}
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
