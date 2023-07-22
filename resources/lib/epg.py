# -*- coding: utf-8 -*-
import xbmc
import time, datetime, random
import resources.lib.common as common
import resources.lib.iptv as iptv

module = 'epg'
profileDir = common.profileDir
epgURLs = ['http://bit.ly/epgfish', 'http://bit.ly/epgzip']

now = int(time.time())

def GetDisplayName(programTime, programName, channelNameFormat):
	if channelNameFormat == 0 or channelNameFormat == 1:
		displayName = ' {0} {1} '.format(programTime, programName)  
	elif channelNameFormat == 2 or channelNameFormat == 3:
		displayName = ' {0} {1} '.format(programName, programTime)
	return displayName
	
def ShowChannelEPG(channel, name='', iconimage='', provider='auto', days=2):
	common.addDir('------- {0} -------'.format(common.GetLabelColor(name, keyColor="chColor", bold=True)), name, 99, iconimage, isFolder=False)
	day = ""
	epgList = GetEPG()
	programs = epgList[channel]
	channelNameFormat = int(common.GetAddonSetting("channelNameFormat"))
	for program in programs:
		if now >= program['end']:
			continue
		startdate = datetime.datetime.fromtimestamp(program["start"]).strftime('%d/%m/%y')
		if startdate != day:
			day = startdate
			dayS = common.GetLabelColor(day, keyColor="prColor", bold=True)
			common.addDir(dayS, 'epg', 99, iconimage, {"Title": dayS}, module=module, isFolder=False)
		start_time = datetime.datetime.fromtimestamp(program["start"]).strftime('%H:%M')
		end_time = datetime.datetime.fromtimestamp(program["end"]).strftime('%H:%M')
		programName = GetDisplayName(common.GetLabelColor('[{0}-{1}]'.format(start_time, end_time), keyColor="timesColor"), common.GetLabelColor(common.encode(program["name"].strip(),'utf-8'), keyColor="prColor", bold=True), channelNameFormat)
		description = common.encode(program["description"].strip(), 'utf-8')
		common.addDir(programName, 'epg', 99, iconimage, {"Title": programName, "Plot": description}, module=module, isFolder=False)

def GetNowEPG():
	epgList = GetEPG()
	for channel in list(epgList.keys()):
		programs = []
		programsCount = len(epgList[channel])
		for i in range(programsCount):
			start = epgList[channel][i]["start"]
			end = epgList[channel][i]["end"]
			if now >= end:
				continue
			if i+1 < programsCount: 
				programs = epgList[channel][i:i+2]
				break
			else:
				programs = epgList[channel][i:i+1]
				break
		epgList[channel] = programs
	return epgList

def GetEPG(deltaInSec=86400):
	epgURL = random.choice(epgURLs)
	epgList = common.GetUpdatedList(common.epgFile, epgURL, headers={'Referer': 'http://idan-{0}.Kodi-{1}.fish'.format(common.AddonVer, common.GetKodiVer())}, deltaInSec=deltaInSec, isZip=True)
	return epgList if len(epgList) > 0 else {}

# Translation of the user interface labels to Portuguese
def SetPortugueseLabels():
	common.addon.setLocalizedString(30001, "EPG")  # Replace 'EPG' with the Portuguese translation
	common.addon.setLocalizedString(30002, "Programas Agora")  # Replace 'Now Programs' with the Portuguese translation
	common.addon.setLocalizedString(30003, "Nenhum programa disponível.")  # Replace 'No program available.' with the Portuguese translation

def Run(name, url, mode, iconimage='', moreData=''):
	if mode == 2:
		days = 2
		provider = 'auto'
		if moreData != '':
			params = moreData.split(';')
			for param in params:
				prm = param.split('=')
				if prm[0] == 'provider':
					provider = prm[1]
				elif prm[0] == 'days':
					days = prm[1]
		ShowChannelEPG(url, name, iconimage, provider, days)
	elif mode == 3:
		GetEPG(deltaInSec=0)
	common.SetViewMode('episodes')  # Replace 'episodes' with the appropriate view mode for the EPG in your skin
	SetPortugueseLabels()  # Call the function to set Portuguese labels

# Assuming you have a function that sets the view mode, replace 'episodes' with the appropriate view mode for the EPG in your skin.
# For example, if your skin uses 'list' as the view mode, change this line to: common.SetViewMode('list')
