import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { PasswordInput } from './index';

const meta: Meta<typeof PasswordInput> = {
  title: 'Components/PasswordInput',
  component: PasswordInput,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  args: { onChange: fn() },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { placeholder: 'Password' } };
export const WithError: Story = { args: { placeholder: 'Password', error: true, helperText: 'Too short' } };
export const Disabled: Story = { args: { placeholder: 'Password', disabled: true } };
