import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { DatePicker } from './index';

const meta: Meta<typeof DatePicker> = {
  title: 'Components/DatePicker',
  component: DatePicker,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  args: { onChange: fn() },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { placeholder: 'Select date' } };
export const WithValue: Story = { args: { value: '2025-01-15' } };
