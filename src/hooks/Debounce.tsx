import { useEffect, useState } from "react";

export function useDebounce<T>(val: T, delay: number) {
  const [debouncedValue, setDebouncedValue] = useState<T>(val);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setDebouncedValue(val);
    }, delay);

    return () => {
      clearTimeout(timeoutId);
    };
  }, [val, delay]);
  return debouncedValue;
}
