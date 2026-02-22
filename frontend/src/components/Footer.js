import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center text-sm text-gray-600">
          <p className="mb-2">
            <strong>Disclaimer:</strong> This tool provides informational guidance and is not a government agency.
            Eligibility varies by program and may require verification by the program provider.
          </p>
          <p>We do not provide medical advice.</p>
          <p className="mt-4 text-gray-500">
            © {new Date().getFullYear()} BenefitPlate. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
