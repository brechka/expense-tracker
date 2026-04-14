import { memo } from 'react';
import type { FC } from 'react';
import type { InputProps } from '../Input';
import { Input } from '../Input';

interface IProps extends InputProps {
  value?: string;
}

/**
 * DatePicker component renders a date input using the Input component.
 * Wraps Input with type="date" for native browser date picking.
 *
 * @example
 * ```tsx
 * <DatePicker placeholder="Pick date" onChange={(val) => console.log(val)} />
 * ```
 */
export const DatePicker: FC<IProps> = memo((props) => {
  return <Input type="date" {...props} />;
});
