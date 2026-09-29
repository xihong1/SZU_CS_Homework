import socket
import os
import struct
import threading
import io
import json
import re
from datetime import datetime
from PIL import Image
from vl2 import main as vl2_main
class ImageUploadVLServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.server_socket = None
        self.model, self.processor, self.fixed_prompt = self.init_vl_model()
        print(f"VL模型已加载，设备: {self.model.device}")
    def init_vl_model(self):
        import torch
        from transformers import AutoModelForVision2Seq, AutoProcessor
        from datetime import datetime
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        MODEL_PATH = "./Qwen3-VL"
        FIXED_PROMPT = f"""你是一个专业的日程管理助手。今天日期是{today_str}。

请分析照片提取日程信息，并严格按照下面的JSON格式输出结果：

如果是活动日程（会议、约会、活动等），使用格式1：
{{"主题": "简要描述", "日期": "YYYY-MM-DD", "开始时间": "HH:MM", "地点": "具体位置", "持续时间": 分钟数, "类型": 1}}

如果是截止任务（提交、交付等），使用格式2：
{{"主题": "简要描述", "日期": "YYYY-MM-DD", "地点": "具体位置", "截止时间": "HH:MM", "类型": 2}}

如果不是日程安排，使用格式3：
{{"类型": 0}}

重要规则：
1. 日期格式必须是YYYY-MM-DD
2. 时间使用24小时制（HH:MM）
3. 持续时间单位是分钟
4. 如果信息缺失，使用"未指定"
5. 只输出JSON，不要有任何其他文字

现在请分析以下图片："""
        try:
            processor = AutoProcessor.from_pretrained(
                MODEL_PATH,
                trust_remote_code=True
            )
            if torch.cuda.is_available():
                print(f"✓ GPU可用: {torch.cuda.get_device_name(0)}")
                device_type = "cuda"
                model = AutoModelForVision2Seq.from_pretrained(
                    MODEL_PATH,
                    torch_dtype=torch.bfloat16,
                    device_map="auto",
                    trust_remote_code=True
                )
            else:
                device_type = "cpu"
                model = AutoModelForVision2Seq.from_pretrained(
                    MODEL_PATH,
                    torch_dtype=torch.float32,
                    device_map="cpu",
                    trust_remote_code=True
                )
            model.eval()
            return model, processor, FIXED_PROMPT
        except Exception as e:
            print(f"加载VL模型失败: {e}")
            if os.path.exists(MODEL_PATH):
                print(f"\n模型目录内容:")
                for item in os.listdir(MODEL_PATH):
                    print(f"  {item}")
            else:
                print(f"\n模型目录不存在: {MODEL_PATH}")
            return None, None, None
    def extract_json_from_text(self, text):
        json_pattern = r'\{[^{}]*\{[^{}]*\}[^{}]*\}|\{[^{}]*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        if matches:
            return max(matches, key=len)
        return text
    def parse_json_response(self, response):
        try:
            json_str = self.extract_json_from_text(response)
            data = json.loads(json_str)
            if "类型" not in data:
                return {"error": "JSON格式错误: 缺少'类型'字段", "raw_response": response}
            event_type = data["类型"]
            if event_type == 1:  # 活动日程
                required_fields = ["主题", "日期", "开始时间", "地点", "持续时间"]
                for field in required_fields:
                    if field not in data:
                        data[field] = "未指定"
            elif event_type == 2:  # 截止任务
                required_fields = ["主题", "日期", "地点", "截止时间"]
                for field in required_fields:
                    if field not in data:
                        data[field] = "未指定"
            elif event_type == 0:
                pass
            else:
                return {"error": f"未知的类型值: {event_type}", "raw_response": response}
            return data
        except json.JSONDecodeError as e:
            return {"error": f"JSON解析错误: {str(e)}", "raw_response": response}
        except Exception as e:
            return {"error": f"处理响应时出错: {str(e)}", "raw_response": response}
    def process_image_with_vl(self, image_bytes, filename):
        if self.model is None or self.processor is None:
            return {"error": "VL模型未正确加载"}

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            print(f"处理图像: {filename}, 尺寸: {image.size}")
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": self.fixed_prompt}
                    ]
                }
            ]
            print("正在处理图像和文本...")
            text = self.processor.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            import torch
            inputs = self.processor(
                images=image,
                text=text,
                return_tensors="pt"
            ).to(self.model.device)
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=False,
                    pad_token_id=self.processor.tokenizer.pad_token_id,
                    eos_token_id=self.processor.tokenizer.eos_token_id,
                )
                generated_text = self.processor.batch_decode(
                    generated_ids,
                    skip_special_tokens=True
                )[0]
                if "<|im_start|>assistant" in generated_text:
                    response = generated_text.split("<|im_start|>assistant\n")[-1].strip()
                else:
                    response = generated_text
                    if "用户:" in response:
                        response = response.split("用户:")[-1].strip()
                    if "assistant:" in response.lower():
                        response = response.split("assistant:", 1)[-1].strip()
                    response = response.replace(self.fixed_prompt, "").strip()
            response = response.strip()
            parsed_result = self.parse_json_response(response)
            if "error" in parsed_result:
                result = {
                    "status": "error",
                    "message": parsed_result["error"],
                    "raw_response": parsed_result.get("raw_response", response)[:500],
                    "filename": filename
                }
            else:
                result = {
                    "status": "success",
                    "message": "图片分析完成",
                    "result": parsed_result,
                    "raw_response": response[:500],  # 只返回前500字符
                    "filename": filename
                }
            return result
        except Exception as e:
            print(f"处理图像时出错: {e}")
            return {"status": "error", "message": f"处理图像时出错: {str(e)}", "filename": filename}
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Socket服务器启动在 {self.host}:{self.port}")
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"\n客户端连接: {client_address}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\n服务器正在关闭...")
        except Exception as e:
            print(f"服务器错误: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        try:
            header = client_socket.recv(8)
            if len(header) < 8:
                print("协议头不完整")
                return
            name_len = struct.unpack('!I', header[:4])[0]
            file_size = struct.unpack('!I', header[4:])[0]
            filename_bytes = b''
            while len(filename_bytes) < name_len:
                chunk = client_socket.recv(name_len - len(filename_bytes))
                if not chunk:
                    break
                filename_bytes += chunk
            if len(filename_bytes) != name_len:
                print("文件名接收不完整")
                return
            filename = filename_bytes.decode('utf-8')
            print(f"接收文件: {filename} ({file_size} bytes)")
            received_size = 0
            file_data = b''
            while received_size < file_size:
                chunk_size = min(4096, file_size - received_size)
                data = client_socket.recv(chunk_size)
                if not data:
                    break
                file_data += data
                received_size += len(data)
                progress = (received_size / file_size) * 100
                print(f"\r接收进度: {progress:.1f}%", end='')
            print()
            if received_size != file_size:
                print(f"文件接收不完整: {received_size}/{file_size} bytes")
                response = {
                    "status": "error",
                    "message": f"文件接收不完整: {received_size}/{file_size} bytes",
                    "filename": filename
                }
                response_data = json.dumps(response).encode('utf-8')
                response_len = len(response_data)
                client_socket.send(struct.pack('!I', response_len))
                client_socket.send(response_data)
                return
            print("开始使用VL模型分析图片...")
            result = self.process_image_with_vl(file_data, filename)
            result_str = json.dumps(result, ensure_ascii=False)
            response_data = result_str.encode('utf-8')
            response_len = len(response_data)
            client_socket.send(struct.pack('!I', response_len))
            client_socket.send(response_data)
            print(f"处理完成")
            if result.get("status") == "success":
                result_data = result.get("result", {})
                event_type = result_data.get("类型", 0)
                if event_type == 0:
                    print("分析结果: 非日程安排")
                elif event_type == 1:
                    subject = result_data.get("主题", "未指定")
                    date = result_data.get("日期", "未指定")
                    time = result_data.get("开始时间", "未指定")
                    print(f"分析结果: 活动日程 - {subject} ({date} {time})")
                elif event_type == 2:
                    subject = result_data.get("主题", "未指定")
                    date = result_data.get("日期", "未指定")
                    deadline = result_data.get("截止时间", "未指定")
                    print(f"分析结果: 截止任务 - {subject} ({date} {deadline})")
            else:
                print(f"分析失败: {result.get('message', '未知错误')}")
        except Exception as e:
            print(f"处理客户端 {client_address} 时出错: {e}")
            # 发送错误响应
            try:
                error_response = {
                    "status": "error",
                    "message": f"服务器处理错误: {str(e)}",
                    "filename": filename if 'filename' in locals() else "未知"
                }
                error_data = json.dumps(error_response).encode('utf-8')
                client_socket.send(struct.pack('!I', len(error_data)))
                client_socket.send(error_data)
            except:
                pass
        finally:
            client_socket.close()
            print(f"客户端断开: {client_address}")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8888
    server = ImageUploadVLServer(HOST, PORT)
    server.start()