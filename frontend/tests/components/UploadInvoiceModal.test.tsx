import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UploadInvoiceModal } from '@/components/UploadInvoiceModal';
import { apiClient } from '@/utils/api';

vi.mock('@/utils/api', () => ({
  apiClient: { post: vi.fn() },
}));

describe('UploadInvoiceModal', () => {
  const mockOnClose = vi.fn();
  const mockOnUploadSuccess = vi.fn();
  const mockOnError = vi.fn();

  beforeEach(() => { vi.clearAllMocks(); });

  it('renders when isOpen is true', () => {
    render(<UploadInvoiceModal isOpen={true} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    expect(screen.getByText('Upload Invoice')).toBeInTheDocument();
    expect(screen.getByText('Drag & drop your invoice image here')).toBeInTheDocument();
    expect(screen.getByText('JPG files up to 5 MB')).toBeInTheDocument();
  });

  it('does not render when isOpen is false', () => {
    render(<UploadInvoiceModal isOpen={false} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    expect(screen.queryByText('Upload Invoice')).not.toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', async () => {
    const user = userEvent.setup();
    render(<UploadInvoiceModal isOpen={true} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    await user.click(screen.getByLabelText('Close modal'));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when cancel button is clicked', async () => {
    const user = userEvent.setup();
    render(<UploadInvoiceModal isOpen={true} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    await user.click(screen.getByText('Cancel'));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('upload button is disabled without file', () => {
    render(<UploadInvoiceModal isOpen={true} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    expect(screen.getByText('Upload & Analyze')).toBeDisabled();
  });

  it('accepts valid JPG file and shows filename', async () => {
    const user = userEvent.setup();
    render(<UploadInvoiceModal isOpen={true} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    const file = new File(['test'], 'invoice.jpg', { type: 'image/jpeg' });
    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    if (input) {
      await user.upload(input, file);
      await waitFor(() => { expect(screen.getByText('invoice.jpg')).toBeInTheDocument(); });
      expect(screen.getByText('Upload & Analyze')).toBeEnabled();
    }
  });

  it('has accessible dialog role', () => {
    render(<UploadInvoiceModal isOpen={true} onClose={mockOnClose} onUploadSuccess={mockOnUploadSuccess} />);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
});
