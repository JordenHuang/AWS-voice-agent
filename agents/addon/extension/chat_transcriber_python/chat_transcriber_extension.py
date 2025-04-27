#
#
# Agora Real Time Engagement
# Created by XinHui Li in 2024-07.
# Copyright (c) 2024 Agora IO. All rights reserved.
#
#
import boto3
import json
from rte import (
    Extension,
    RteEnv,
    Cmd,
    Data,
    StatusCode,
    CmdResult,
    MetadataInfo,
)
import time
from .pb import chat_text_pb2 as pb
from .log import logger

CMD_NAME_FLUSH = "flush"

TEXT_DATA_TEXT_FIELD = "text"
TEXT_DATA_FINAL_FIELD = "is_final"
TEXT_DATA_STREAM_ID_FIELD = "stream_id"
TEXT_DATA_END_OF_SEGMENT_FIELD = "end_of_segment"

# record the cached text data for each stream id
cached_text_map = {}
bedrock_client = boto3.client("bedrock", region_name="us-west-2")  # 替換為你的區域

class ChatTranscriberExtension(Extension):
    def on_start(self, rte: RteEnv) -> None:
        logger.info("on_start")
        rte.on_start_done()

    def on_stop(self, rte: RteEnv) -> None:
        logger.info("on_stop")
        rte.on_stop_done()

    def on_cmd(self, rte: RteEnv, cmd: Cmd) -> None:
        logger.info("on_cmd")
        cmd_json = cmd.to_json()
        logger.info("on_cmd json: {}".format(cmd_json))

        cmd_result = CmdResult.create(StatusCode.OK)
        cmd_result.set_property_string("detail", "success")
        rte.return_result(cmd_result, cmd)
#hhhhhh
    def on_data(self, rte: RteEnv, data: Data) -> None:
        logger.info(f"on_data")
        try:
            text = data.get_property_string(TEXT_DATA_TEXT_FIELD)
            stream_id = data.get_property_int(TEXT_DATA_STREAM_ID_FIELD)
            end_of_segment = data.get_property_bool(TEXT_DATA_END_OF_SEGMENT_FIELD)
        except Exception as e:
            logger.exception(f"Error extracting data: {e}")
            return

        if end_of_segment:
            # 傳遞文本給 Bedrock 代理人
            try:
                response = bedrock_client.agrent(
                    modelId="7CPKIKVOEF",  # 替換為你的代理人 ID
                    contentType="application/json",
                    body=json.dumps({"inputText": text}),
                )
                agent_response = json.loads(response["body"])["outputText"]
                logger.info(f"Bedrock agent response: {agent_response}")

                # 將回應文本傳給 TTS 模組
                self.forward_to_tts(rte, agent_response, stream_id)

            except Exception as e:
                logger.error(f"Error invoking Bedrock agent: {e}")

        try:
            text = data.get_property_string(TEXT_DATA_TEXT_FIELD)
        except Exception as e:
            logger.exception(
                f"on_data get_property_string {TEXT_DATA_TEXT_FIELD} error: {e}"
            )
            return

        try:
            final = data.get_property_bool(TEXT_DATA_FINAL_FIELD)
        except Exception as e:
            logger.exception(
                f"on_data get_property_bool {TEXT_DATA_FINAL_FIELD} error: {e}"
            )
            return

        try:
            stream_id = data.get_property_int(TEXT_DATA_STREAM_ID_FIELD)
        except Exception as e:
            logger.exception(
                f"on_data get_property_int {TEXT_DATA_STREAM_ID_FIELD} error: {e}"
            )
            return

        try:
            end_of_segment = data.get_property_bool(TEXT_DATA_END_OF_SEGMENT_FIELD)
        except Exception as e:
            logger.exception(
                f"on_data get_property_bool {TEXT_DATA_END_OF_SEGMENT_FIELD} error: {e}"
            )
            return

        logger.debug(
            f"on_data {TEXT_DATA_TEXT_FIELD}: {text} {TEXT_DATA_FINAL_FIELD}: {final} {TEXT_DATA_STREAM_ID_FIELD}: {stream_id} {TEXT_DATA_END_OF_SEGMENT_FIELD}: {end_of_segment}"
        )

        # We cache all final text data and append the non-final text data to the cached data
        # until the end of the segment.
        if end_of_segment:
            if stream_id in cached_text_map:
                text = cached_text_map[stream_id] + text
                del cached_text_map[stream_id]
        else:
            if final:
                if stream_id in cached_text_map:
                    text = cached_text_map[stream_id] + text

                cached_text_map[stream_id] = text

        pb_text = pb.Text(
            uid=stream_id,
            data_type="transcribe",
            texttime=int(time.time() * 1000),  # Convert to milliseconds
            words=[
                pb.Word(
                    text=text,
                    is_final=end_of_segment,
                ),
            ],
        )

        try:
            pb_serialized_text = pb_text.SerializeToString()
        except Exception as e:
            logger.warning(f"on_data SerializeToString error: {e}")
            return

        try:
            # convert the origin text data to the protobuf data and send it to the graph.
            rte_data = Data.create("data")
            rte_data.set_property_buf("data", pb_serialized_text)
            rte.send_data(rte_data)
            logger.info("data sent")
        except Exception as e:
            logger.warning(f"on_data new_data error: {e}")
            return

    def forward_to_tts(self, rte: RteEnv, text: str, stream_id: int):
        # 創建新數據傳遞到 TTS
        data = Data.create("tts_input")
        data.set_property_string("text", text)
        data.set_property_int("stream_id", stream_id)
        rte.send_data(data)
