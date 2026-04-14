import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Input } from './index';

const meta: Meta<typeof Input> = {
  title: 'Components/Input',
  component: Input,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  args: { onChange: fn() },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { placeholder: 'Enter text...' } };
export const WithValue: Story = { args: { placeholder: 'Email', defaultValue: 'user@example.com' } };
export const WithError: Story = { args: { placeholder: 'Email', error: true, helperText: 'Email is required' } };
export const Disabled: Story = { args: { placeholder: 'Disabled', disabled: true } };
