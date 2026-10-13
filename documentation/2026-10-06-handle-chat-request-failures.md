# Handle Chat Request Failures

**Suggested commit message:** `Handle chat request failures`  
**Date:** 2026-10-06

## Summary

This change adds a fallback assistant message when the frontend cannot complete or parse the `/chat` API request, and tracks whether the request is in progress. It also removes the unused default React import from `src/App.tsx`.

## What Changed

- Added an `isLoading` state value in `src/components/chatInputForm/chatInputForm.tsx`. `sendPrompt` sets it to `true` before requesting the API and resets it to `false` in a `finally` block, including when the request or response handling throws.
- Wrapped the `/chat` fetch and response processing in a `try`/`catch`. When an error is thrown, the catch appends an assistant `ChatMessage` with the text `"I couldnt get a valid response from the API. Please try again later"`.
- Kept the existing success and solver-failure handling: successful solver results are converted to text, while unsuccessful results use `solver.error_message` or the existing fallback.
- Changed the React import in `src/App.tsx` to import only the named `useState` hook.

## Request Flow

1. `handleSend` trims the input, appends the user message, clears the input, and calls `sendPrompt`.
2. `sendPrompt` sets `isLoading` and POSTs `{ message }` to `http://127.0.0.1:8000/chat`.
3. A successfully processed response is appended as an assistant message. If the fetch, JSON parsing, or response processing throws, a fallback assistant message is appended instead.
4. The `finally` block resets `isLoading` after either outcome.

## Current Limitations

- `isLoading` is not currently rendered or used to disable the input or send button, so users do not see a loading indicator and can submit another message while a request is pending.
- The catch handles thrown errors but the code does not explicitly check `response.ok` or validate the response shape before reading `data.solver`.
- The fallback message currently contains the spelling `"couldnt"` without an apostrophe.

## Verification

- The behavior described above was traced by reading the staged changes in `src/App.tsx` and `src/components/chatInputForm/chatInputForm.tsx`.
- No automated frontend tests or build results are recorded for this change.
