import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Button } from './index';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    type: { control: 'select', options: ['button', 'submit', 'reset'] },
    disabled: { control: 'boolean' },
    children: { control: 'text' },
  },
  args: { onClick: fn() },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { children: 'Button', disabled: false, type: 'button' } };
export const Disabled: Story = { args: { children: 'Disabled Button', disabled: true } };
export const Submit: Story = { args: { children: 'Submit', type: 'submit' } };
