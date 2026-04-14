import type { Meta, StoryObj } from '@storybook/react';
import { Icon } from './index';

const meta: Meta<typeof Icon> = {
  title: 'Components/Icon',
  component: Icon,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    icon: { control: 'select', options: ['mobile', 'credit', 'shopping', 'restaurant', 'transport', 'utility', 'hobby', 'subscription', 'debt', 'other_payment'] },
    color: { control: 'select', options: ['grey', 'white'] },
    size: { control: 'number' },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { icon: 'mobile', size: 32, color: 'grey' } };
export const Shopping: Story = { args: { icon: 'shopping', size: 32, color: 'grey' } };
export const WhiteOnDark: Story = {
  args: { icon: 'restaurant', size: 32, color: 'white' },
  decorators: [(Story) => <div style={{ background: '#333', padding: 16, borderRadius: 8 }}><Story /></div>],
};
