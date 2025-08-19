import os
import json
import zipfile
import re
import traceback
from io import BytesIO
from configparser import ConfigParser

def safe_open_jar(file_path):
    """安全打开可能包含特殊字符或非标准压缩的JAR文件"""
    try:
        # 使用二进制模式读取，避免编码问题
        with open(file_path, 'rb') as f:
            jar_data = BytesIO(f.read())
        return zipfile.ZipFile(jar_data)
    except Exception as e:
        print(f"无法打开文件 {file_path}: {str(e)}")
        return None

def parse_toml_content(content):
    """解析mods.toml内容，处理多行值和特殊格式"""
    mod_info = {"modid": None, "name": None, "version": None}
    
    # 简化TOML解析，处理常见格式
    lines = content.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # 处理多行字符串
        if line.startswith('modId=') and '"""' in line:
            modid_match = re.search(r'modId\s*=\s*"""([\s\S]*?)"""', content, re.DOTALL)
            if modid_match:
                mod_info["modid"] = modid_match.group(1).strip()
        elif line.startswith('displayName=') and '"""' in line:
            name_match = re.search(r'displayName\s*=\s*"""([\s\S]*?)"""', content, re.DOTALL)
            if name_match:
                mod_info["name"] = name_match.group(1).strip()
        elif line.startswith('version=') and '"""' in line:
            version_match = re.search(r'version\s*=\s*"""([\s\S]*?)"""', content, re.DOTALL)
            if version_match:
                mod_info["version"] = version_match.group(1).strip()
        else:
            # 处理单行值
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                if key == 'modId':
                    mod_info["modid"] = value
                elif key == 'displayName':
                    mod_info["name"] = value
                elif key == 'version':
                    mod_info["version"] = value
                    
    return mod_info

def parse_mcmod_info(content):
    """解析旧版Forge的mcmod.info文件"""
    try:
        # 尝试解析JSON格式
        if content.strip().startswith('['):
            data = json.loads(content)
            if data and isinstance(data, list) and len(data) > 0:
                return {
                    "modid": data[0].get("modid"),
                    "name": data[0].get("name"),
                    "version": data[0].get("version")
                }
        # 尝试解析属性文件格式
        else:
            config = ConfigParser()
            config.read_string('[DEFAULT]\n' + content)
            return {
                "modid": config.get('DEFAULT', 'modid', fallback=None),
                "name": config.get('DEFAULT', 'name', fallback=None),
                "version": config.get('DEFAULT', 'version', fallback=None)
            }
    except:
        return None

def extract_mod_info(file_path):
    """从JAR文件中提取模组信息，支持多种格式和特殊情况"""
    jar = None
    try:
        jar = safe_open_jar(file_path)
        if not jar:
            return None
            
        mod_infos = []
        
        # 1. 尝试解析Fabric/Quilt模组
        fabric_files = [f for f in jar.namelist() if f.endswith('fabric.mod.json')]
        for fabric_file in fabric_files:
            try:
                with jar.open(fabric_file) as f:
                    fabric_data = json.load(f)
                    # 处理多模组打包
                    if isinstance(fabric_data, list):
                        for mod in fabric_data:
                            mod_infos.append({
                                "modid": mod.get("id"),
                                "name": mod.get("name"),
                                "version": mod.get("version")
                            })
                    else:
                        mod_infos.append({
                            "modid": fabric_data.get("id"),
                            "name": fabric_data.get("name"),
                            "version": fabric_data.get("version")
                        })
            except:
                pass
                
        if mod_infos:
            return mod_infos
        
        # 2. 尝试解析Forge/NeoForge模组 (mods.toml)
        toml_files = [f for f in jar.namelist() if 'mods.toml' in f.lower()]
        for toml_file in toml_files:
            try:
                with jar.open(toml_file) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    mod_info = parse_toml_content(content)
                    if mod_info["modid"]:
                        mod_infos.append(mod_info)
            except:
                pass
                
        if mod_infos:
            return mod_infos
            
        # 3. 尝试解析旧版Forge模组 (mcmod.info)
        mcmod_files = [f for f in jar.namelist() if 'mcmod.info' in f.lower()]
        for mcmod_file in mcmod_files:
            try:
                with jar.open(mcmod_file) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    mod_info = parse_mcmod_info(content)
                    if mod_info and mod_info["modid"]:
                        mod_infos.append(mod_info)
            except:
                pass
                
        # 4. 回退方案：尝试从文件名提取信息
        if not mod_infos:
            filename = os.path.basename(file_path)
            # 尝试从文件名解析modid和版本
            match = re.match(r'^(?P<modid>[a-z0-9_]+)-(?P<version>[0-9\.]+)', filename, re.IGNORECASE)
            if match:
                mod_infos.append({
                    "modid": match.group("modid"),
                    "name": match.group("modid"),  # 使用modid作为名称
                    "version": match.group("version")
                })
            else:
                # 最终回退：使用文件名作为modid
                modid = os.path.splitext(filename)[0].lower().replace(' ', '_').replace('-', '_')
                mod_infos.append({
                    "modid": modid,
                    "name": modid,  # 使用modid作为名称
                    "version": "unknown"
                })
                
        return mod_infos
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        traceback.print_exc()
        return None
    finally:
        if jar:
            jar.close()

def scan_mods_directory(directory):
    """扫描目录并收集所有模组信息"""
    mods_list = []
    skipped_files = []
    processed_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jar', '.zip', '.disabled')):
                full_path = os.path.join(root, file)
                print(f"处理文件: {file}")
                
                mod_infos = extract_mod_info(full_path)
                if mod_infos:
                    for mod_info in mod_infos:
                        if mod_info.get("modid"):
                            # 仅保留modid, name, version三个字段
                            clean_info = {
                                "modid": mod_info["modid"],
                                "name": mod_info.get("name", mod_info["modid"]),
                                "version": mod_info.get("version", "unknown")
                            }
                            mods_list.append(clean_info)
                            processed_count += 1
                        else:
                            skipped_files.append(file)
                else:
                    skipped_files.append(file)
    
    print(f"\n扫描完成: 处理了 {processed_count} 个模组, 跳过了 {len(skipped_files)} 个文件")
    if skipped_files:
        print("跳过的文件:")
        for f in skipped_files[:10]:  # 最多显示10个
            print(f" - {f}")
        if len(skipped_files) > 10:
            print(f" - 和另外 {len(skipped_files)-10} 个文件...")
    
    return mods_list

def main():
    # 配置扫描目录
    mods_dir = input("请输入模组目录路径: ").strip()
    if not os.path.isdir(mods_dir):
        print("错误: 指定的路径不是有效目录")
        return
    
    # 扫描模组
    print(f"\n开始扫描目录: {mods_dir}")
    mods_data = scan_mods_directory(mods_dir)
    
    # 写入JSON文件
    output_file = os.path.join(os.getcwd(), 'mods.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mods_data, f, ensure_ascii=False, indent=4)
    
    print(f"\n成功找到 {len(mods_data)} 个模组")
    print(f"结果已保存至: {output_file},请自行批量替换mandatory和\字段为空")

if __name__ == "__main__":
    main()