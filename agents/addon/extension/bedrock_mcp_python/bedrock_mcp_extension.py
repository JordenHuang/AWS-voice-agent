#
#
# Agora Real Time Engagement
# Created by XinHui Li in 2024.
# Copyright (c) 2024 Agora IO. All rights reserved.
#
#
from threading import Thread
from rte import (
    Extension,
    RteEnv,
    Cmd,
    Data,
    StatusCode,
    CmdResult,
)
from .bedrock_mcp import BedrockMcp, BedrockMcpConfig
from .log import logger
from .utils import get_micro_ts, parse_sentence


CMD_IN_FLUSH = "flush"
CMD_OUT_FLUSH = "flush"
DATA_IN_TEXT_DATA_PROPERTY_TEXT = "text"
DATA_IN_TEXT_DATA_PROPERTY_IS_FINAL = "is_final"
DATA_OUT_TEXT_DATA_PROPERTY_TEXT = "text"
DATA_OUT_TEXT_DATA_PROPERTY_TEXT_END_OF_SEGMENT = "end_of_segment"

PROPERTY_API_KEY = "api_key"  # Optional
PROPERTY_BASE_URL = "base_url"  # Required
PROPERTY_GREETING = "greeting"  # Optional
PROPERTY_MAX_MEMORY_LENGTH = "max_memory_length"  # Optional
PROPERTY_MAX_TOKENS = "max_tokens"  # Optional
PROPERTY_MODEL = "model"  # Optional
PROPERTY_PROMPT = "prompt"  # Optional
PROPERTY_TEMPERATURE = "temperature"  # Optional
PROPERTY_TOP_P = "top_p"  # Optional
PROPERTY_TOP_K = "top_k"  # Optional
PROPERTY_MCP_SERVER_IDS = "mcp_server_ids"  # Optional

class BedrockMcpExtension(Extension):
    memory = []
    max_memory_length = 10
    outdate_ts = 0
    bedrock_mcp = None

    def on_start(self, rte: RteEnv) -> None:
        logger.info("BedrockMcpExtension on_start")
        # Prepare configuration
        bedrock_mcp_config = BedrockMcpConfig.default_config()

        for key in [PROPERTY_API_KEY, PROPERTY_BASE_URL, PROPERTY_GREETING, PROPERTY_MODEL, 
                    PROPERTY_PROMPT, PROPERTY_MCP_SERVER_IDS]:
            try:
                val = rte.get_property_string(key)
                if val:
                    bedrock_mcp_config.__setattr__(key, val)
            except Exception as e:
                logger.warning(f"get_property_string optional {key} failed, err: {e}")

        for key in [PROPERTY_TEMPERATURE, PROPERTY_TOP_P, PROPERTY_TOP_K]:
            try:
                bedrock_mcp_config.__setattr__(key, float(rte.get_property_float(key)))
            except Exception as e:
                logger.warning(f"get_property_float optional {key} failed, err: {e}")

        for key in [PROPERTY_MAX_MEMORY_LENGTH, PROPERTY_MAX_TOKENS]:
            try:
                bedrock_mcp_config.__setattr__(key, int(rte.get_property_int(key)))
            except Exception as e:
                logger.warning(f"get_property_int optional {key} failed, err: {e}")

        bedrock_mcp_config.validate()
        logger.warning(bedrock_mcp_config.__dict__)

        # Create BedrockMcp instance
        self.bedrock_mcp = BedrockMcp(bedrock_mcp_config)
        logger.info(f"newBedrockMcp succeed with max_tokens: {bedrock_mcp_config.max_tokens}, model: {bedrock_mcp_config.model}")

        # Send greeting if available
        greeting = rte.get_property_string(PROPERTY_GREETING)
        if greeting:
            try:
                output_data = Data.create("text_data")
                output_data.set_property_string(DATA_OUT_TEXT_DATA_PROPERTY_TEXT, greeting)
                output_data.set_property_bool(DATA_OUT_TEXT_DATA_PROPERTY_TEXT_END_OF_SEGMENT, True)
                rte.send_data(output_data)
                logger.info(f"greeting [{greeting}] sent")
            except Exception as e:
                logger.error(f"greeting [{greeting}] send failed, err: {e}")

        rte.on_start_done()

    def on_stop(self, rte: RteEnv) -> None:
        logger.info("BedrockMcpExtension on_stop")
        rte.on_stop_done()

    def on_cmd(self, rte: RteEnv, cmd: Cmd) -> None:
        logger.info("BedrockMcpExtension on_cmd")
        cmd_json = cmd.to_json()
        logger.info(f"BedrockMcpExtension on_cmd json: {cmd_json}")

        cmd_name = cmd.get_name()

        if cmd_name == CMD_IN_FLUSH:
            self.outdate_ts = get_micro_ts()
            cmd_out = Cmd.create(CMD_OUT_FLUSH)
            rte.send_cmd(cmd_out, None)
            logger.info(f"BedrockMcpExtension on_cmd sent flush")
        else:
            logger.info(f"BedrockMcpExtension on_cmd unknown cmd: {cmd_name}")
            cmd_result = CmdResult.create(StatusCode.ERROR)
            cmd_result.set_property_string("detail", "unknown cmd")
            rte.return_result(cmd_result, cmd)
            return

        cmd_result = CmdResult.create(StatusCode.OK)
        cmd_result.set_property_string("detail", "success")
        rte.return_result(cmd_result, cmd)

    def on_data(self, rte: RteEnv, data: Data) -> None:
        """
        on_data receives data from rte graph.
        current supported data:
          - name: text_data
            example:
            {name: text_data, properties: {text: "hello"}
        """
        logger.info(f"BedrockMcpExtension on_data")

        # Assume 'data' is an object from which we can get properties
        try:
            is_final = data.get_property_bool(DATA_IN_TEXT_DATA_PROPERTY_IS_FINAL)
            if not is_final:
                logger.info("ignore non-final input")
                return
        except Exception as e:
            logger.error(f"on_data get_property_bool {DATA_IN_TEXT_DATA_PROPERTY_IS_FINAL} failed, err: {e}")
            return

        # Get input text
        try:
            input_text = data.get_property_string(DATA_IN_TEXT_DATA_PROPERTY_TEXT)
            if not input_text:
                logger.info("ignore empty text")
                return
            logger.info(f"on_data input text: [{input_text}]")
        except Exception as e:
            logger.error(f"on_data get_property_string {DATA_IN_TEXT_DATA_PROPERTY_TEXT} failed, err: {e}")
            return

        # Prepare memory
        if len(self.memory) > self.max_memory_length:
            self.memory.pop(0)
        self.memory.append({"role": "user", "content": input_text})

        def chat_completions_stream_worker(start_time, input_text, memory):
            try:
                logger.info(f"chat_completions_stream_worker for input text: [{input_text}] memory: {memory}")

                # Get result from AI
                resp = self.bedrock_mcp.get_chat_completions_stream(memory)
                if resp is None:
                    logger.info(f"chat_completions_stream_worker for input text: [{input_text}] failed")
                    return

                sentence = ""
                full_content = ""
                first_sentence_sent = False

                for chat_completions in resp:
                    # allow 100ms buffer time, in case interruptor's flush cmd comes just after on_data event
                    if (start_time + 100_000) < self.outdate_ts:
                        logger.info(f"chat_completions_stream_worker recv interrupt and flushing for input text: [{input_text}], startTs: {start_time}, outdateTs: {self.outdate_ts}, delta > 100ms")
                        break

                    if (len(chat_completions.choices) > 0 and chat_completions.choices[0].delta.content is not None):
                        content = chat_completions.choices[0].delta.content
                    else:
                        content = ""

                    full_content += content

                    while True:
                        sentence, content, sentence_is_final = parse_sentence(sentence, content)

                        if len(sentence) == 0 or not sentence_is_final:
                            logger.info(f"sentence {sentence} is empty or not final")
                            break

                        sentence = sentence.replace('<thinking>', '').replace('</thinking>', '')

                        logger.info(f"chat_completions_stream_worker recv for input text: [{input_text}] got sentence: [{sentence}]")

                        # send sentence
                        try:
                            output_data = Data.create("text_data")
                            output_data.set_property_string(DATA_OUT_TEXT_DATA_PROPERTY_TEXT, sentence)
                            output_data.set_property_bool(DATA_OUT_TEXT_DATA_PROPERTY_TEXT_END_OF_SEGMENT, False)
                            rte.send_data(output_data)
                            logger.info(f"chat_completions_stream_worker recv for input text: [{input_text}] sent sentence [{sentence}]")
                        except Exception as e:
                            logger.error(f"chat_completions_stream_worker recv for input text: [{input_text}] send sentence [{sentence}] failed, err: {e}")
                            break

                        sentence = ""
                        if not first_sentence_sent:
                            first_sentence_sent = True
                            logger.info(f"chat_completions_stream_worker recv for input text: [{input_text}] first sentence sent, first_sentence_latency {get_micro_ts() - start_time}ms")

                # remember response as assistant content in memory
                memory.append({"role": "assistant", "content": full_content})

                # send end of segment
                try:
                    output_data = Data.create("text_data")
                    output_data.set_property_string(DATA_OUT_TEXT_DATA_PROPERTY_TEXT, sentence)
                    output_data.set_property_bool(DATA_OUT_TEXT_DATA_PROPERTY_TEXT_END_OF_SEGMENT, True)
                    rte.send_data(output_data)
                    logger.info(f"chat_completions_stream_worker for input text: [{input_text}] end of segment with sentence [{sentence}] sent")
                except Exception as e:
                    logger.error(f"chat_completions_stream_worker for input text: [{input_text}] end of segment with sentence [{sentence}] send failed, err: {e}")

            except Exception as e:
                logger.error(f"chat_completions_stream_worker for input text: [{input_text}] failed, err: {e}")

        # Start thread to request and read responses from BedrockMcp
        start_time = get_micro_ts()
        thread = Thread(
            target=chat_completions_stream_worker,
            args=(start_time, input_text, self.memory),
        )
        thread.start()
        logger.info(f"BedrockMcpExtension on_data end")
