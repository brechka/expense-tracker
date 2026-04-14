import type { Meta, StoryObj } from '@storybook/react';
import { InputLabel } from './index';

const meta: Meta<typeof InputLabel> = {
  title: 'Components/InputLabel',
  component: InputLabel,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { children: 'Email', htmlFor: 'email' } };
