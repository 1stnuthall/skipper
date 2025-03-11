// Contents of ./functions/hello_world.ts
import { DefineFunction, Schema, SlackFunction } from "deno-slack-sdk/mod.ts";

export const HelloWorldFunctionDef = DefineFunction({
  callback_id: "hello_world_function",
  title: "Hello World",
  source_file: "functions/hello_world.ts",
  input_parameters: {
    properties: {},
    required: [],
  },
  output_parameters: {
    properties: {
      message: {
        type: Schema.types.string,
        description: "Hello world message",
      },
    },
    required: ["message"],
  },
});

export default SlackFunction(
  HelloWorldFunctionDef,
  () => {
    return {
      outputs: { message: "Hello World!" },
    };
  },
);