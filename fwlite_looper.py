import sys
import numpy as np
import cPickle

import ROOT
from DataFormats.FWLite import Events, Handle

events = Events(sys.argv[1])

objects = {
    "kt4PFJets": Handle('std::vector<reco::PFJet>'),
    "kt4GenJets": Handle('std::vector<reco::GenJet>'),
    "generalTracks": Handle('std::vector<reco::Track>'),
}

def get_objects(event, name):
    event.getByLabel (name, objects[name])
    objs = objects[name].product()
    return objs


MAX_EVENTS = 10000
JETS_PER_EVENT = 10
TRACKS_PER_EVENT = 50
MAX_JETS = MAX_EVENTS * JETS_PER_EVENT
MAX_TRACKS = MAX_EVENTS * TRACKS_PER_EVENT

jet_array = np.zeros(MAX_JETS, dtype=[
    ("px", "f4"),
    ("py", "f4"),
    ("pz", "f4"),
    ("e", "f4"),
    ("event", "i4")]
)
ijet = 0

track_array = np.zeros(MAX_TRACKS, dtype=[
    ("px", "f4"),
    ("py", "f4"),
    ("pz", "f4"),
    ("qoverp", "f4"),
    ("lambda", "f4"),
    ("event", "i4")]
)
itrack = 0

for iEv, event in enumerate(events):
    if iEv >= MAX_EVENTS:
        break
    if iEv%100 == 0:
        print iEv

    jets = get_objects(event, "kt4PFJets")
    for jet in jets[:JETS_PER_EVENT]:
        jet_array["px"][ijet] = jet.px()
        jet_array["py"][ijet] = jet.py()
        jet_array["pz"][ijet] = jet.pz()
        jet_array["e"][ijet] = jet.energy()
        jet_array["event"][ijet] = iEv

        ijet += 1
        if ijet >= MAX_JETS:
            raise Exception("out of jet bounds")

    tracks = get_objects(event, "generalTracks")
    for track in tracks[:TRACKS_PER_EVENT]:
        track_array["px"][itrack] = track.px()
        track_array["py"][itrack] = track.py()
        track_array["pz"][itrack] = track.pz()
        track_array["qoverp"][itrack] = track.qoverp()
        track_array["lambda"][itrack] = getattr(track, "lambda")()
        track_array["event"][itrack] = iEv
        itrack += 1
        if itrack >= MAX_TRACKS:
            raise Exception("out of track bounds")
    
    #genjets = get_objects(event, "kt4GenJets")
    #print "genjets={0}".format(len(genjets))
    #for jet in genjets[:5]:
    #    constituents = []
    #    for gc in jet.getGenConstituents():
    #        pdg = gc.pdgId()
    #        status = gc.status()
    #        pt = gc.pt()
    #        constituents += [(pdg, status, pt)]
    #    print constituents

np.save("jets.npy", jet_array)
np.save("tracks.npy", track_array)
